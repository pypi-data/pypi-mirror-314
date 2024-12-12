# Unstructured Expanded

The `unstructured_expanded` library is a wrapper around the `unstructured` open source library to add image-extraction capabilities to the API.

Its only purpose is to provide a more complete API for the `unstructured` library, since the library maintainers of the open source project
have chosen to lock image extraction for office documents behind a paywall.

## Quick-Start

This library is meant to be used in conjunction with the `unstructured` library.

Versions of this library are equivalent to the `unstructured` library version they are based on.

```shell
# Install the variant of unstructured with everything you need support for
pip install unstructured["all-docs"]

# Install the unstructured_expanded library on top of it
pip install unstructured_expanded
```

## License

See the licensing information in the [LICENSE](LICENSE) file.

## Citation

If you use this library in your research, please include a citation:

```bibtex
@misc{unstructured_expanded,
  title={Unstructured_expanded: A Python Library for Extracting Text and Images from Documents using the unstructured API.},
  author={Kogan, Isaac},
  year={2024},
  url={https://github.com/isaackogan/unstructured_expanded}
}
```