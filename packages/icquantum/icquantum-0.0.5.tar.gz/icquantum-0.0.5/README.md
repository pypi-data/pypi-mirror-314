# icquantum

This project has tools for building and running Quantum Circuit simulations. It is used in some ICHEC projects and [demos](https://git.ichec.ie/performance/recipes/quantum).

## Installing ##

The package is available on PyPI, you can install it with:

``` shell
pip install icquantum
```

## Features ##

### Benchmarking ###

You can run a named quantum circuit from a benchmark as follows:

``` shell
icquantum benchmark --circuit sample
```

At the moment the library has a single built-in circuit `sample` and the [MQT Bench](https://github.com/cda-tum/mqt-bench) benchmark. Circuits for the later are namespaced with `mqtbench:`, so you can launch one with:

``` shell
icquantum benchmark --circuit mqtbench:dj
```

for example. The are many other command line arguments allowing control over number of circuits and iterations run and Qiskit runtime settings. They can be seen with:

``` shell
icquantum benchmark --help
```

## License ##

This software is Copyright ICHEC 2024 and can be re-used under the terms of the GPL v3+. See the included `LICENSE` file for details.
