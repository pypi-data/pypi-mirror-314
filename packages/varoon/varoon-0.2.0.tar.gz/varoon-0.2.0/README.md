# varoon

A tool for checking reflected parameters in URLs. This tool is as same as [Kxss](https://github.com/Emoe/kxss). I tried to rewrite it in python.

## Installation

```bash
pipx install varoon
```

### Usage

```bash
echo "www.target.website" | waybackurls | parshu -x | bhedak "hello" | uro | varoon
```

### Sample Output

```css
echo "www.target.website" | waybackurls | parshu -x | bhedak "hello" | uro | varoon

URL: http://www.target.website/Search.asp?q=hello Param: tfSearch Unfiltered: [" < > $ | ( ) ` : ; { }]
URL: http://www.target.website/id?account=hello Param: account Unfiltered: [" < > $ | ( ) ` : ; { }]
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
