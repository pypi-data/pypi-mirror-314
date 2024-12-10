use std::{
    path::{Path, PathBuf},
    sync::{RwLock, RwLockReadGuard, RwLockWriteGuard},
};

/// Persist offers an encapsulation of the durable storage for T.
///
pub(crate) struct Persist<T: rkyv::Archive> {
    path: PathBuf,
    db: heed::Database<heed::types::Bytes, heed::types::Bytes>,
    env: RwLock<Env>,
    _phantom: std::marker::PhantomData<T>,
}

impl<
        T: rkyv::Archive
            + for<'a> rkyv::Serialize<
                rkyv::rancor::Strategy<
                    rkyv::ser::Serializer<
                        rkyv::util::AlignedVec,
                        rkyv::ser::allocator::ArenaHandle<'a>,
                        rkyv::ser::sharing::Share,
                    >,
                    rkyv::rancor::Error,
                >,
            >,
    > Persist<T>
{
    pub(crate) fn new(path: &str, filename: &str) -> Result<Self, FactorGraphStoreError> {
        std::fs::create_dir_all(path)?;
        let path = Path::new(path);
        let path = path.join(filename);
        let env = unsafe {
            let mut env_options = heed::EnvOpenOptions::new();
            env_options.flags(
                heed::EnvFlags::MAP_ASYNC
                    | heed::EnvFlags::NO_SUB_DIR
                    | heed::EnvFlags::WRITE_MAP
                    | heed::EnvFlags::NO_LOCK
                    | heed::EnvFlags::NO_READ_AHEAD,
            );
            #[cfg(target_pointer_width = "32")]
            env_options.map_size(1024 * 1024 * 1024);
            #[cfg(target_pointer_width = "64")]
            env_options.map_size(1024 * 1024 * 1024 * 1024);
            env_options.open(&path)?
        };

        let mut wtxn = env.write_txn()?;
        let db = env
            .database_options()
            .types::<heed::types::Bytes, heed::types::Bytes>()
            .create(&mut wtxn)?;
        wtxn.commit()?;
        let env = RwLock::new(env);
        Ok(Persist::<T> {
            path,
            db,
            env,
            _phantom: std::marker::PhantomData,
        })
    }
    pub(crate) fn open_read(&self) -> Result<ReadTransaction<'_>, heed::Error> {
        let guard = Box::new(self.env.read().unwrap());
        let guard_ptr = NonNull::new(Box::into_raw(guard)).unwrap();
        Ok(ReadTransaction::new(
            guard_ptr,
            unsafe { guard_ptr.as_ref() }.read_txn()?
        ))
    }
    pub(crate) fn open_write(&self) -> Result<WriteTransaction<'_>, heed::Error> {
        let guard = Box::new(self.env.write().unwrap());
        let guard_ptr = NonNull::new(Box::into_raw(guard)).unwrap();
        Ok(WriteTransaction::new(
            guard_ptr,
            unsafe { guard_ptr.as_ref() }.write_txn()?)
        )
    }
    pub(crate) fn get<'a>(
        &self,
        transaction: &'a impl CanRead<T>,
        key: &[u8],
    ) -> Option<&'a <T as rkyv::Archive>::Archived> {
        transaction.get(self.db, key)
    }
    pub(crate) fn insert(
        &self,
        transaction: &mut WriteTransaction,
        key: &[u8],
        value: T,
    ) -> Result<(), heed::Error> {
        let buf = rkyv::to_bytes::<rkyv::rancor::Error>(&value).unwrap();
        self.db
            .put(transaction.transaction.as_mut().unwrap(), key, &buf)
    }

    #[allow(dead_code)] // used through trait
    pub(crate) fn remove(&self, transaction: &mut WriteTransaction, key: &[u8]) {
        self.db
            .delete(transaction.transaction.as_mut().unwrap(), key)
            .unwrap();
    }
    pub(crate) fn clear(
        &self,
        transaction: &mut WriteTransaction,
    ) -> Result<(), FactorGraphStoreError> {
        if let Some(tx) = transaction.transaction.as_mut() {
            self.db.clear(tx).map_err(|e| e.into())
        } else {
            Ok(()) // No-op
        }
    }
    pub(crate) fn iter<'a>(
        &self,
        transaction: &'a impl CanRead<T>,
    ) -> impl Iterator<Item = (&'a [u8], &'a <T as rkyv::Archive>::Archived)>
    where
        <T as rkyv::Archive>::Archived: 'a,
    {
        transaction.iter(self.db)
    }

    #[allow(dead_code)] // used through trait
    pub(crate) fn len<R: CanRead<T>>(&self, transaction: &R) -> Result<u64, R::Error> {
        transaction.len(self.db)
    }

    /// Delete the actual backing file. Consumes the Persist object.
    pub(crate) fn delete(self) -> Result<(), std::io::Error> {
        std::fs::remove_file(self.path)
    }
}

use crate::error::FactorGraphStoreError;
use heed::{Env, RoTxn, RwTxn};
use std::ptr::NonNull;

pub(crate) struct ReadTransaction<'a> {
    guard: NonNull<RwLockReadGuard<'a, Env>>,
    // this is an Option because we need to take it out of the struct before dropping the guard
    transaction: Option<RoTxn<'a>>,
}
impl<'a> ReadTransaction<'a> {
    /// Ensure that we cannot create a ReadTransaction from a None transaction
    fn new(guard: NonNull<RwLockReadGuard<'a, Env>>, transaction: RoTxn<'a>) -> Self {
        ReadTransaction {
            guard,
            transaction: Some(transaction),
        }
    }
}

pub(crate) struct WriteTransaction<'a> {
    guard: NonNull<RwLockWriteGuard<'a, Env>>,
    transaction: Option<RwTxn<'a>>,
}

impl<'a> WriteTransaction<'a> {
    /// Ensure that we cannot create a WriteTransaction from a None transaction
    fn new(guard: NonNull<RwLockWriteGuard<'a, Env>>, transaction: RwTxn<'a>) -> Self {
        WriteTransaction {
            guard,
            transaction: Some(transaction),
        }
    }

    #[allow(dead_code)] // used in a test
    pub(crate) fn abort(mut self) {
        let tx = self.transaction.take();
        if let Some(tx) = tx {
            tx.abort();
        }
    }
}

pub(crate) trait CanRead<
    T: rkyv::Archive
        + for<'a> rkyv::Serialize<
            rkyv::rancor::Strategy<
                rkyv::ser::Serializer<
                    rkyv::util::AlignedVec,
                    rkyv::ser::allocator::ArenaHandle<'a>,
                    rkyv::ser::sharing::Share,
                >,
                rkyv::rancor::Error,
            >,
        >,
>
{
    type Error;

    #[allow(dead_code)]
    fn len(&self, db: heed::Database<heed::types::Bytes, heed::types::Bytes>) -> Result<u64, Self::Error>;
    fn get(
        &self,
        db: heed::Database<heed::types::Bytes, heed::types::Bytes>,
        key: &[u8],
    ) -> Option<&<T as rkyv::Archive>::Archived>;
    fn iter<'a>(
        &'a self,
        db: heed::Database<heed::types::Bytes, heed::types::Bytes>,
    ) -> impl Iterator<Item = (&'a [u8], &'a <T as rkyv::Archive>::Archived)>
    where
        <T as rkyv::Archive>::Archived: 'a;
}
impl<
        T: rkyv::Archive
            + for<'a> rkyv::Serialize<
                rkyv::rancor::Strategy<
                    rkyv::ser::Serializer<
                        rkyv::util::AlignedVec,
                        rkyv::ser::allocator::ArenaHandle<'a>,
                        rkyv::ser::sharing::Share,
                    >,
                    rkyv::rancor::Error,
                >,
            >,
    > CanRead<T> for ReadTransaction<'_>
{
    type Error = heed::Error;

    #[allow(dead_code)] // used through trait
    fn len(&self, db: heed::Database<heed::types::Bytes, heed::types::Bytes>) -> Result<u64, Self::Error> {
        db.len(self.transaction.as_ref().unwrap())
    }
    fn get(
        &self,
        db: heed::Database<heed::types::Bytes, heed::types::Bytes>,
        key: &[u8],
    ) -> Option<&<T as rkyv::Archive>::Archived> {
        match db.get(self.transaction.as_ref().unwrap(), key) {
            Ok(Some(buf)) => Some(unsafe { rkyv::access_unchecked(buf) }),
            Ok(None) => None,
            Err(_) => None,
        }
    }
    fn iter<'a>(
        &'a self,
        db: heed::Database<heed::types::Bytes, heed::types::Bytes>,
    ) -> impl Iterator<Item = (&'a [u8], &'a <T as rkyv::Archive>::Archived)>
    where
        <T as rkyv::Archive>::Archived: 'a,
    {
        db.iter(self.transaction.as_ref().unwrap())
            .unwrap()
            .map(|result| {
                let (key, value) = result.unwrap();
                (key, unsafe { rkyv::access_unchecked(value) })
            })
    }
}
impl<
        T: rkyv::Archive
            + for<'a> rkyv::Serialize<
                rkyv::rancor::Strategy<
                    rkyv::ser::Serializer<
                        rkyv::util::AlignedVec,
                        rkyv::ser::allocator::ArenaHandle<'a>,
                        rkyv::ser::sharing::Share,
                    >,
                    rkyv::rancor::Error,
                >,
            >,
    > CanRead<T> for WriteTransaction<'_>
{
    type Error = heed::Error;

    fn len(&self, db: heed::Database<heed::types::Bytes, heed::types::Bytes>) -> Result<u64, Self::Error> {
        db.len(self.transaction.as_ref().unwrap())
    }

    fn get(
        &self,
        db: heed::Database<heed::types::Bytes, heed::types::Bytes>,
        key: &[u8],
    ) -> Option<&<T as rkyv::Archive>::Archived> {
        match db.get(self.transaction.as_ref().unwrap(), key) {
            Ok(Some(buf)) => Some(unsafe { rkyv::access_unchecked(buf) }),
            Ok(None) => None,
            Err(_) => None,
        }
    }
    fn iter<'a>(
        &'a self,
        db: heed::Database<heed::types::Bytes, heed::types::Bytes>,
    ) -> impl Iterator<Item = (&'a [u8], &'a <T as rkyv::Archive>::Archived)>
    where
        <T as rkyv::Archive>::Archived: 'a,
    {
        db.iter(self.transaction.as_ref().unwrap())
            .unwrap()
            .map(|result| {
                let (key, value) = result.unwrap();
                (key, unsafe { rkyv::access_unchecked(value) })
            })
    }
}

impl<'a> Drop for ReadTransaction<'a> {
    fn drop(&mut self) {
        if let Some(transaction) = self.transaction.take() {
            let _ = transaction.commit();
        }
        unsafe {
            drop(Box::from_raw(self.guard.as_ptr()));
        }
    }
}
impl<'a> Drop for WriteTransaction<'a> {
    fn drop(&mut self) {
        if let Some(transaction) = self.transaction.take() {
            let _ = transaction.commit();
        }
        unsafe {
            drop(Box::from_raw(self.guard.as_ptr()));
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::loader::GraphNode;
    use crate::types::Factor;

    /// Description: Tests if we can determine if two instances of the same file can be opened
    /// Objectives: Two instances of the same file can be opened
    #[test]
    fn test_multiple_instance_same_file() {
        let persist1 =
            Persist::<GraphNode<Factor>>::new("test_multiple_instance_same_file", "nodes").unwrap();
        let persist2 =
            Persist::<GraphNode<Factor>>::new("test_multiple_instance_same_file", "nodes").unwrap();

        let mut transaction1 = persist1.open_write().unwrap();
        let mut transaction2 = persist2.open_write().unwrap();

        let value = GraphNode {
            input: vec!["cloudy".to_string()],
            contents: Factor::default(),
        };
        assert!(persist1.insert(&mut transaction1, &[0], value).is_ok());

        drop(transaction1);

        // should error because different persist instance
        let value = GraphNode {
            input: vec!["cloudy".to_string()],
            contents: Factor::default(),
        };
        assert!(persist2.get(&transaction2, &[0]).is_none());
        assert!(persist2.insert(&mut transaction2, &[1], value).is_err());

        drop(transaction2);

        std::fs::remove_dir_all("test_multiple_instance_same_file").unwrap();
    }

    /// Description: Tests if we can persist a factor graph. Saves and loads.
    /// Objectives: Factor graph is saved and loaded correctly.
    #[test]
    fn test_persist() {
        let persist = Persist::<GraphNode<Factor>>::new("test_persist", "nodes").unwrap();

        let mut transaction = persist.open_write().unwrap();
        let value = GraphNode {
            input: vec!["cloudy".to_string()],
            contents: Factor::default(),
        };
        persist.insert(&mut transaction, &[0], value).unwrap();
        drop(transaction);

        let transaction = persist.open_read().unwrap();
        let value = persist.get(&transaction, &[0]).unwrap();
        assert_eq!(value.input[0], "cloudy");
        drop(transaction);

        let mut transaction = persist.open_write().unwrap();
        persist.remove(&mut transaction, &[0]);
        assert!(persist.get(&transaction, &[0]).is_none());
        drop(transaction);

        drop(persist);
        std::fs::remove_dir_all("test_persist").unwrap();
    }

    /// Description: Tests if we can clear a persisted graph
    /// Objectives:
    ///  - Graph can be cleared
    ///  - Graph has no data after clear
    ///  - Graph can be re-used after clear
    #[test]
    fn test_persist_clear() {
        let persist = Persist::<GraphNode<Factor>>::new("factor_graph_data/test_persist_clear", "nodes").unwrap();

        let mut transaction = persist.open_write().unwrap();
        let value = GraphNode {
            input: vec!["cloudy".to_string()],
            contents: Factor::default(),
        };
        persist
            .insert(&mut transaction, &[0], value)
            .expect("can insert into persistence");
        drop(transaction);

        let mut transaction = persist.open_write().unwrap();
        persist.clear(&mut transaction).expect("Can clear");
        assert_eq!(persist.len(&transaction).unwrap(), 0);
        drop(transaction);

        //test that db still works after clear
        let mut transaction = persist.open_write().unwrap();
        let value = GraphNode {
            input: vec!["cloudy".to_string()],
            contents: Factor::default(),
        };
        persist.insert(&mut transaction, &[0], value).unwrap();
        drop(transaction);

        let transaction = persist.open_read().unwrap();
        let value = persist.get(&transaction, &[0]).unwrap();
        assert_eq!(value.input[0], "cloudy");
        drop(transaction);

        drop(persist);
        std::fs::remove_dir_all("factor_graph_data/test_persist_clear").expect("can delete test directory");
    }

    /// Description: Tests if we can remove a single node from a persisted graph
    /// Objectives: Node can be removed from graph
    #[test]
    fn test_persist_remove() {
        let persist = Persist::<GraphNode<Factor>>::new("factor_graph_data/test_persist_remove", "nodes").unwrap();

        let mut transaction = persist.open_write().expect("can open txn");
        let value = GraphNode {
            input: vec!["cloudy".to_string()],
            contents: Factor::default(),
        };
        persist.insert(&mut transaction, &[0], value).unwrap();
        assert!(persist.get(&transaction, &[0]).is_some());
        drop(transaction);

        let mut transaction = persist.open_write().expect("can open txn");
        persist.remove(&mut transaction, &[0]);
        assert!(persist.get(&transaction, &[0]).is_none());
        drop(transaction);

        drop(persist);
        std::fs::remove_dir_all("factor_graph_data/test_persist_remove").unwrap();
    }

    #[test]
    fn test_txn_abort() {
        let persist = Persist::<GraphNode<Factor>>::new("factor_graph_data/test_txn_abort", "nodes").unwrap();

        let mut transaction = persist.open_write().expect("can open txn");
        let value = GraphNode {
            input: vec!["cloudy".to_string()],
            contents: Factor::default(),
        };
        persist.insert(&mut transaction, &[0], value).unwrap();
        drop(transaction);

        let mut transaction = persist.open_write().expect("can open txn");
        let value2 = GraphNode {
            input: vec!["sunny".to_string()],
            contents: Factor::default(),
        };
        persist.insert(&mut transaction, &[1], value2).unwrap();
        transaction.abort();

        let target_value = GraphNode {
            input: vec!["cloudy".to_string()],
            contents: Factor::default(),
        };
        let transaction = persist.open_read().expect("can open txn");
        let value_archived = persist.get(&transaction, &[0]).unwrap();
        let value = rkyv::deserialize::<GraphNode<Factor>, rkyv::rancor::Error>(value_archived).expect("can deserialize");
        assert_eq!(value, target_value);
        drop(transaction);
    }
}
