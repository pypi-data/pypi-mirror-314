# Changelog

## [1.5.0](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.20...v1.5.0) (2024-12-09)


### Features

* expose pyvfg.__version__ to consumers of pyvfg ([#119](https://github.com/VersesTech/genius-agent-factor-graph/issues/119)) ([2e4d8d7](https://github.com/VersesTech/genius-agent-factor-graph/commit/2e4d8d784c7d2c73d61ebeddde700c8b1ba14b3b))


### Bug Fixes

* use single maturin job for publish ([#121](https://github.com/VersesTech/genius-agent-factor-graph/issues/121)) ([b54934c](https://github.com/VersesTech/genius-agent-factor-graph/commit/b54934c560bb3df4a85cb935ed73627484abd8f0))

## [1.4.20](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.19...v1.4.20) (2024-12-09)


### Bug Fixes

* publish to public pypi ([#118](https://github.com/VersesTech/genius-agent-factor-graph/issues/118)) ([e59aa5e](https://github.com/VersesTech/genius-agent-factor-graph/commit/e59aa5ed607d91d15d9151d58247a82837e000bb))

## [1.4.19](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.18...v1.4.19) (2024-12-06)


### Bug Fixes

* call_once_force allows Once to continue even if poisoned without immediately panicing. ([#116](https://github.com/VersesTech/genius-agent-factor-graph/issues/116)) ([7f8654a](https://github.com/VersesTech/genius-agent-factor-graph/commit/7f8654a2cab5b31b66224f29c6c3b0d2c353bdde))

## [1.4.18](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.17...v1.4.18) (2024-11-26)


### Bug Fixes

* fix panic on empty values for a factor (which is incorrect in validation, and fails validation, but *no crashes ever* is the target) ([#112](https://github.com/VersesTech/genius-agent-factor-graph/issues/112)) ([2425d82](https://github.com/VersesTech/genius-agent-factor-graph/commit/2425d827f9847e374f8433a2fb5227efe62b12ee))

## [1.4.17](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.16...v1.4.17) (2024-11-19)


### Bug Fixes

* propagates error types as their respective types to python ([#110](https://github.com/VersesTech/genius-agent-factor-graph/issues/110)) ([c36ae98](https://github.com/VersesTech/genius-agent-factor-graph/commit/c36ae980fe8300d0b65a2f9ea2e2898933238725))

## [1.4.16](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.15...v1.4.16) (2024-11-12)


### Bug Fixes

* provide nice names for python types. ([#108](https://github.com/VersesTech/genius-agent-factor-graph/issues/108)) ([4346f6e](https://github.com/VersesTech/genius-agent-factor-graph/commit/4346f6e652538aacbeaa8af0d529a20d5b8f48e6))

## [1.4.15](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.14...v1.4.15) (2024-11-04)


### Bug Fixes

* fix lint errors ([#105](https://github.com/VersesTech/genius-agent-factor-graph/issues/105)) ([0e76845](https://github.com/VersesTech/genius-agent-factor-graph/commit/0e768453835d799a1d9792be02e50f5b65be9d3b))

## [1.4.14](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.13...v1.4.14) (2024-11-04)


### Bug Fixes

* dedupe macos builds ([#100](https://github.com/VersesTech/genius-agent-factor-graph/issues/100)) ([ca44ea3](https://github.com/VersesTech/genius-agent-factor-graph/commit/ca44ea3b03c194a137b4ba3226f9bbf90ae4fce9))

## [1.4.13](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.12...v1.4.13) (2024-11-04)


### Bug Fixes

* vfg example ([#99](https://github.com/VersesTech/genius-agent-factor-graph/issues/99)) ([76cceac](https://github.com/VersesTech/genius-agent-factor-graph/commit/76cceacbda8cf8fce0445af476c7fdd8e3322664))

## [1.4.12](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.11...v1.4.12) (2024-11-04)


### Miscellaneous Chores

* fix macos builds ([#97](https://github.com/VersesTech/genius-agent-factor-graph/issues/97)) ([0f40f3b](https://github.com/VersesTech/genius-agent-factor-graph/commit/0f40f3b9ba7f3fde767316452934e48f31c152b0))

## [1.4.11](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.10...v1.4.11) (2024-11-04)


### Bug Fixes

* include examples in json schema ([#95](https://github.com/VersesTech/genius-agent-factor-graph/issues/95)) ([5e5a67a](https://github.com/VersesTech/genius-agent-factor-graph/commit/5e5a67a7cb408c06680d85c8d61ffcfccd7c09c5))

## [1.4.10](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.9...v1.4.10) (2024-11-04)


### Bug Fixes

* Remove InvalidVariableItemCount error ([#93](https://github.com/VersesTech/genius-agent-factor-graph/issues/93)) ([0e5a950](https://github.com/VersesTech/genius-agent-factor-graph/commit/0e5a950ba240604a399b77c3f63d8e4a58468ad0))

## [1.4.9](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.8...v1.4.9) (2024-11-01)


### Bug Fixes

* validation issues ([#91](https://github.com/VersesTech/genius-agent-factor-graph/issues/91)) ([028f0b9](https://github.com/VersesTech/genius-agent-factor-graph/commit/028f0b9f0b82e231fc723200c6e3b8056313cafb))

## [1.4.8](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.7...v1.4.8) (2024-11-01)


### Bug Fixes

* instantiate tokio runtime during telemetry init ([#89](https://github.com/VersesTech/genius-agent-factor-graph/issues/89)) ([d095a85](https://github.com/VersesTech/genius-agent-factor-graph/commit/d095a85173e2b4dc4b8810b55d14331622392c1d))

## [1.4.7](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.6...v1.4.7) (2024-11-01)


### Bug Fixes

* regression: replace_graph() should call validate_graph() ([#87](https://github.com/VersesTech/genius-agent-factor-graph/issues/87)) ([a9bf5d0](https://github.com/VersesTech/genius-agent-factor-graph/commit/a9bf5d04f82db0acc1a318d0cb0e72f36b6e9ba4))

## [1.4.6](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.5...v1.4.6) (2024-11-01)


### Miscellaneous Chores

* release 1.4.6 ([3b52cf1](https://github.com/VersesTech/genius-agent-factor-graph/commit/3b52cf17e2184364f35ad81c50ebdaea1fd2f9ba))

## [1.4.5](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.4...v1.4.5) (2024-10-31)


### Bug Fixes

* [GPAI-135] manually drop open file to support running DB migration tests under Windows ([#78](https://github.com/VersesTech/genius-agent-factor-graph/issues/78)) ([fa9963c](https://github.com/VersesTech/genius-agent-factor-graph/commit/fa9963c48bc7e3f59a6e882d52ec8324e9f1a7be))

## [1.4.4](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.3...v1.4.4) (2024-10-30)


### Bug Fixes

* random example ([#66](https://github.com/VersesTech/genius-agent-factor-graph/issues/66)) ([7b7d5a6](https://github.com/VersesTech/genius-agent-factor-graph/commit/7b7d5a6dc2f8436448987cc3313b279a10eee51f))
* test for all possible enum types ([#80](https://github.com/VersesTech/genius-agent-factor-graph/issues/80)) ([90322d7](https://github.com/VersesTech/genius-agent-factor-graph/commit/90322d7bb0e7eac50db7e8237a83f75bef71fffe))

## [1.4.3](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.2...v1.4.3) (2024-10-30)	


### Bug Fixes	

* exposes python types for Variable ([#73](https://github.com/VersesTech/genius-agent-factor-graph/issues/73)) ([1068add](https://github.com/VersesTech/genius-agent-factor-graph/commit/1068addaa9a532b54dc7ec92a558e11591c4d39f))	
* updated pydantic and pyi files to contain the correct version. updated docs on the changepoints for the future. ([#77](https://github.com/VersesTech/genius-agent-factor-graph/issues/77)) ([640e5c8](https://github.com/VersesTech/genius-agent-factor-graph/commit/640e5c89960e07ea3b82c463b4104946177e9d68))	

## [1.4.2](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.1...v1.4.2) (2024-10-29)


### Bug Fixes

* GPAI-103 automatically call init_tracing() during a FactorGraphStore::new() ([1106623](https://github.com/VersesTech/genius-agent-factor-graph/commit/1106623c869252ffb800057270830208d5b169a4))

## [1.4.1](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.4.0...v1.4.1) (2024-10-29)


### Bug Fixes

* variable role and factor role are optional in json; are now specified as loaded-as-default and skip-if-none ([#71](https://github.com/VersesTech/genius-agent-factor-graph/issues/71)) ([d0d86cf](https://github.com/VersesTech/genius-agent-factor-graph/commit/d0d86cfaba6271b7095a5243e0055b4676374481))

## [1.4.0](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.3.0...v1.4.0) (2024-10-28)


### Features

* [GPAI-128] VFGv0.3.0 support ([#69](https://github.com/VersesTech/genius-agent-factor-graph/issues/69)) ([3f58a99](https://github.com/VersesTech/genius-agent-factor-graph/commit/3f58a99d25f85ee5d7c72c311395146f42dbf638))

## [1.3.0](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.2.0...v1.3.0) (2024-10-28)


### Features

* GPAI-96 3rd pass. rename genius-agent-message-bus-client to genius-agent-factor-graph in tracer ([3b359a3](https://github.com/VersesTech/genius-agent-factor-graph/commit/3b359a33c9eca7ce0cd03c4a1374b4e1a7a192d5))

## [1.2.0](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.1.2...v1.2.0) (2024-10-25)


### Features

* expose validate graph ([#61](https://github.com/VersesTech/genius-agent-factor-graph/issues/61)) ([6ec6431](https://github.com/VersesTech/genius-agent-factor-graph/commit/6ec6431b8ba29cee474271e9ff67daf86cb23add))

## [1.1.2](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.1.1...v1.1.2) (2024-10-23)


### Miscellaneous Chores

* fix release assets ([#57](https://github.com/VersesTech/genius-agent-factor-graph/issues/57)) ([cc8238d](https://github.com/VersesTech/genius-agent-factor-graph/commit/cc8238d1f470200b39e3c389004f793f835a395d))

## [1.1.1](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.1.0...v1.1.1) (2024-10-22)


### Miscellaneous Chores

* add python stub files ([#51](https://github.com/VersesTech/genius-agent-factor-graph/issues/51)) ([8fb98f0](https://github.com/VersesTech/genius-agent-factor-graph/commit/8fb98f0a8d9038a8aa0fee847022ef0192f0e8b0))

## [1.1.0](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.0.0...v1.1.0) (2024-10-22)


### Features

* GPAI-96 1st pass Implement Open Telemetry on the Factor Graph Store ([5024a35](https://github.com/VersesTech/genius-agent-factor-graph/commit/5024a359aac989e225a0f130c0ce5c2589e5ecb5))
* GPAI-96 2nd pass Implement Open Telemetry on the Factor Graph Store ([d77dfc1](https://github.com/VersesTech/genius-agent-factor-graph/commit/d77dfc1f5ef3cc000ee504af1db7508c98f9e448))

## [1.0.0](https://github.com/VersesTech/genius-agent-factor-graph/compare/v1.0.0...v1.0.0) (2024-10-18)


### Features

* Add dockerfile [GPFGS-45]  ([#28](https://github.com/VersesTech/genius-agent-factor-graph/issues/28)) ([b028605](https://github.com/VersesTech/genius-agent-factor-graph/commit/b028605cf73cc82b6beafc0458b40055051be744))
* add WIT bindings + message-bus ([#15](https://github.com/VersesTech/genius-agent-factor-graph/issues/15)) ([ae8067c](https://github.com/VersesTech/genius-agent-factor-graph/commit/ae8067c9bfc8862a769c19fa5e12a0a8f03330f7))
* Expose ADR[#1](https://github.com/VersesTech/genius-agent-factor-graph/issues/1) as top-level library ([#10](https://github.com/VersesTech/genius-agent-factor-graph/issues/10)) ([6e81bda](https://github.com/VersesTech/genius-agent-factor-graph/commit/6e81bda47d172d9b3b3a16ec6a3aa72a55fff8fb))
* Factor graph types crate exposed as a separable crate ([#11](https://github.com/VersesTech/genius-agent-factor-graph/issues/11)) ([5007900](https://github.com/VersesTech/genius-agent-factor-graph/commit/50079007b11b920dcce75229f23de4a7336b502b))
* GPFGS-24 - handle each command having a separate topic, refactor and optimise handler code ([#24](https://github.com/VersesTech/genius-agent-factor-graph/issues/24)) ([3e951ab](https://github.com/VersesTech/genius-agent-factor-graph/commit/3e951abd5cc6acac892ce19b1c48854fbfe8dc20))
* GPFGS-26 - add vfg validation ([#14](https://github.com/VersesTech/genius-agent-factor-graph/issues/14)) ([7a28588](https://github.com/VersesTech/genius-agent-factor-graph/commit/7a2858883ba52ec2a74637442bbf84d4185e7c00))
* GPFGS-39 - set graph with validation ([#26](https://github.com/VersesTech/genius-agent-factor-graph/issues/26)) ([fd474aa](https://github.com/VersesTech/genius-agent-factor-graph/commit/fd474aa64ea25563f888f20b85ceafdaf8eab60a))
* NATS Integration [GPFGS-46] [GPFGS-47] ([#29](https://github.com/VersesTech/genius-agent-factor-graph/issues/29)) ([de44e84](https://github.com/VersesTech/genius-agent-factor-graph/commit/de44e843f29010571484af17dfa35b537eab3e4e))
* Persistent index [GPFGS-27] ([#9](https://github.com/VersesTech/genius-agent-factor-graph/issues/9)) ([052aef1](https://github.com/VersesTech/genius-agent-factor-graph/commit/052aef165e9e7852fcd0e781a292cae4136b6d88))
* Python bindings for VFG Library ([#41](https://github.com/VersesTech/genius-agent-factor-graph/issues/41)) ([2adcd8d](https://github.com/VersesTech/genius-agent-factor-graph/commit/2adcd8da2ebfa82fb9f327b298c1fc3e39ee07c8))


### Bug Fixes

* Align with new types from PR[#39](https://github.com/VersesTech/genius-agent-factor-graph/issues/39) on genius-agent-common ([#47](https://github.com/VersesTech/genius-agent-factor-graph/issues/47)) ([ee1bb00](https://github.com/VersesTech/genius-agent-factor-graph/commit/ee1bb000e2f27ec84506c03ddee42ab6078decd5))
* can now replace graph twice between gets [GPFGS-52] ([#37](https://github.com/VersesTech/genius-agent-factor-graph/issues/37)) ([3789222](https://github.com/VersesTech/genius-agent-factor-graph/commit/3789222fa2e4fd3d0168b031b036b09fea87630c))
* document and cleanup ([#22](https://github.com/VersesTech/genius-agent-factor-graph/issues/22)) ([f2bea23](https://github.com/VersesTech/genius-agent-factor-graph/commit/f2bea232bba462a7c50644cd5ab3d2de0871ba7d))
* fix of PR[#52](https://github.com/VersesTech/genius-agent-factor-graph/issues/52) -- do not re-use db names ([#38](https://github.com/VersesTech/genius-agent-factor-graph/issues/38)) ([6f4bcfe](https://github.com/VersesTech/genius-agent-factor-graph/commit/6f4bcfe4bf17b8898a874cc5a9458966a12fc0cb))
* fixed equality; removed TODOs ([#31](https://github.com/VersesTech/genius-agent-factor-graph/issues/31)) ([64a08ad](https://github.com/VersesTech/genius-agent-factor-graph/commit/64a08ade0414f6d17e29804320722ca3bc90a2c6))
* rust-toolchain.toml ([#20](https://github.com/VersesTech/genius-agent-factor-graph/issues/20)) ([ee19c44](https://github.com/VersesTech/genius-agent-factor-graph/commit/ee19c44ab120f038fd0b23bb23a82ec776d3f769))
* updated dependency on genius-agent-common to f14e043fbd3ef553da142b8c3da869033274398c ([#43](https://github.com/VersesTech/genius-agent-factor-graph/issues/43)) ([1d775e3](https://github.com/VersesTech/genius-agent-factor-graph/commit/1d775e300a5740a44fcbe5b49606ab3914204bb1))
* Updated protos and did a few adjustments ([#45](https://github.com/VersesTech/genius-agent-factor-graph/issues/45)) ([30609df](https://github.com/VersesTech/genius-agent-factor-graph/commit/30609df5ecefaef8c91375865d9633f8077d32cd))


### Miscellaneous Chores

* release 0.2.4 ([6644205](https://github.com/VersesTech/genius-agent-factor-graph/commit/664420501781e4da95022f64e74996ee0da73720))
