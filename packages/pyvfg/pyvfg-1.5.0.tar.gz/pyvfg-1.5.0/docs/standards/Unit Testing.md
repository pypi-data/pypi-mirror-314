# Unit Tests

## Purpose
This standard identifies the "definition of done" for unit tests, to ensure that unit tests are comprehensive, complete, and well documented


## Summary

* `cargo clippy`  reports no errors, or the code is commented where overrides are necessary as to why the override is required
*  Unit tests must be documented with:
    * A descritpive name
    * A description of the scenario being tested.
    * Outcomes expected
    * How the data associated with the test verifies the outcomes
    * In line comments for clarity
    * Use of good error messages for ```assert!()```  macros can replace inline comments
* Unit tests must test all accessible parts of the code
    * Each function in the unit must be tested
    * Success and failure paths
    * Be sure to test edge cases
* Unit tests must be self contained
    * Should not depend on previous tests
    * Should not affect other tests
    * Where feasible, should be able to be run in parallel
    * Should use mocks, stubs or faces for any dependencies the unit under test might have
* Other considerations
    * Tests should yield the same results every time they are run
    * Tests should run fast, or include comments as to why they might not run fast (large data, etc) 

* Remember:
    * Write code that is unit testable.  We've all heard the excuse "this isn't unit testable"
    * The definition of done is that the unit tests are included as part of the Pull Request


## Example

Given the below sample code:
```rust
// Define a struct ListItem with two fields: name and value
struct ListItem {
    name: String,
    value: i32,
}

// Implement a method new for ListItem
impl ListItem {
    fn new(name: &str, value: i32) -> ListItem {
        ListItem {
            name: name.to_string(),
            value,
        }
    }
}

// Define a struct MyList with a single field: items
pub struct MyList {
    items: Vec<ListItem>,
}

// Implement methods for MyList
impl MyList {
    // Implement a method new for MyList
    fn new() -> MyList {
        MyList { items: Vec::new() }
    }

    // adds an item to the list
    // note that you can have multiple items with the same name
    fn add(&mut self, name: &str, value: i32) {
        self.items.push(ListItem::new(name, value));
    }

    // fetches an item from the list by name
    // returns None if the item is not found
    // returns Some(item) if the item is found, but will return only the first item with the name
    fn fetch(&self, name: &str) -> Option<&ListItem> {
        self.items.iter().find(|i| i.name == name)
    }

    // removes an item from the list by name
    // returns None if the item is not found
    // returns Some(item) if the item is found, but will return only the first item with the name
    fn remove(&mut self, name: &str) -> Option<ListItem> {
        let pos = self.items.iter().position(|i| i.name == name);
        match pos {
            Some(i) => Some(self.items.remove(i)),
            None => None,
        }
    }
}
```

Here's a comprehensive unit test that meets the above criteria
```rust
#[cfg(test)]
mod tests {
    use super::*;

    // Description : This test checks that the add method adds an item to the list
    // Objective: Verify that the basic add function works
    //            Verify that the length of the list matches the number of items added
    #[test]
    fn test_add_basic() {
        let mut list = MyList::new();
        list.add("one", 1);
        list.add("two", 2);
        list.add("three", 3);

        // Either the comments or the assert_eq! macro can be used to describe the test outcome
        // length should be 3
        assert_eq!(list.items.len(), 3);
        assert_eq!(list.items.len(), 3, "Length should be 3");
    }

    // Description:  This test checks that the add method adds an item to the list with multiple items with the same name
    // Objective: Verify that we can add multiple items with the same name
    //            Verify that the length of the list is 6, the number of items added
    #[test]
    fn test_add_same_name() {
        let mut list = MyList::new();
        // add a bunch of items, some with the same name
        list.add("one", 1);
        list.add("two", 2);
        list.add("three", 3);
        list.add("one", 11);
        list.add("two", 12);
        list.add("three", 13);

        // Either the comments or the assert_eq! macro can be used to describe the test outcome
        // length should be 6
        assert_eq!(list.items.len(), 6);
        assert_eq!(list.items.len(), 6, "Length should be 6");
    }

    // Description: This test checks that the fetch method returns the correct item
    //              This test assumes that the add method works correctly
    // Objectives: Verify that the fetch operation works with a simple list
    //             Verify the value of the first fetched item ("two") is 2
    //             Verify the value of the second fetched item ("four") is None, since no items with the name "four" were added
    #[test]
    fn test_fetch_basic() {
        let mut list = MyList::new();
        list.add("one", 1);
        list.add("two", 2);
        list.add("three", 3);
        assert_eq!(list.fetch("two").unwrap().value, 2);
        assert_eq!(list.fetch("four").is_none(), true);
    }

    // Description: This test checks that the fetch method returns the correct item
    //              This test assumes that the add method works correctly
    //              This is adds multiple items with the same name to the list
    // Objective: Verify that fetch operation works when you have a list with multiples of the same name
    //            Verify the value of the first fetched item ("two") is 2, the first added item with the name "two"
    //            Verify the value of the second fetched item ("four") is None, since no items with the name "four" were added
    #[test]
    fn test_fetch_advanced() {
        let mut list = MyList::new();
        list.add("one", 1);
        list.add("two", 2);
        list.add("three", 3);
        list.add("one", 11);
        list.add("two", 12);
        list.add("three", 13);
        assert_eq!(list.fetch("two").unwrap().value, 2, "Value should be 2");
        assert_eq!(
            list.fetch("four").is_none(),
            true,
            "Value should be None since no item with the name four was added"
        );
    }

    // Description: This test checks that the remove method removes the correct item
    //              This test assumes that the add method works correctly
    //              This is a basic test that doesn't include multiple items with the same name
    // Objective: Verify that the remove operation works with a simple list
    //            Verify the value of the removed item is 2, the value of the item with the name "two"
    //            Verify the length of the list is 2, the number of items after removing the item with the name "two"
    //            Verify the item which is removed ("four") is None, since no items with the name "four" were added
    //            Verify The length of the list is 2, the number of items after removing the item with the name "four"
    #[test]
    fn test_remove_basic() {
        let mut list = MyList::new();
        list.add("one", 1);
        list.add("two", 2);
        list.add("three", 3);
        assert_eq!(list.remove("two").unwrap().value, 2, "Value should be 2");
        assert_eq!(list.items.len(), 2, "Length should be 2");

        // remove an item that doesn't exist value should be None
        assert_eq!(
            list.remove("four").is_none(),
            true,
            "Value should be None since no item with the name four was added"
        );
        assert_eq!(list.items.len(), 2, "Length should still be 2");
    }

    // Description: This test checks that the remove method removes the correct item
    //              This test assumes that the add method works correctly
    //              This is a more advanced test that includes multiple items with the same name
    // Objective: Verify that the remove operation works with a list that has multiple items with the same name
    //            Verify The item which is removed ("two") is the first added item with the name "two" and has the value of 2
    //            Verify The length of the list is 5, the number of items after removing the item with the name "two"
    //            Verify The item which is removed ("two") is the second added item with the name "two" and has the value of 12
    //            Verify The length of the list is 4, the number of items after removing the second item with the name "two"
    //            Verify The item which is removed ("four") is None, since no items with the name "four" were added
    //            Verify The length of the list is 4, the number of items after removing the item with the name "four"
    #[test]
    fn test_remove_advanced() {
        let mut list = MyList::new();
        list.add("one", 1);
        list.add("two", 2);
        list.add("three", 3);
        list.add("one", 11);
        list.add("two", 12);
        list.add("three", 13);

        // remove the first item with the name "two" value should be 2
        assert_eq!(list.remove("two").unwrap().value, 2, "Value should be 2");

        assert_eq!(list.items.len(), 5, "Length should be 5");

        // remove the second item with the name "two" value should be 12
        assert_eq!(list.remove("two").unwrap().value, 12, "Value should be 12");

        // length should be 4
        assert_eq!(list.items.len(), 4, "Length should be 4");

        // remove an item that doesn't exist value should be None
        assert_eq!(list.remove("four").is_none(), true, "Value should be None");
        assert_eq!(list.items.len(), 4, "Length should still be 4");
    }
}

```