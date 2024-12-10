# Font RPM Spec Generator
[![pip version badge](https://img.shields.io/pypi/v/fontrpmspec)](https://pypi.org/project/fontrpmspec/)
[![tag badge](https://img.shields.io/github/v/tag/fedora-i18n/font-rpm-spec-generator)](https://github.com/fedora-i18n/font-rpm-spec-generator/tags)
[![license badge](https://img.shields.io/github/license/fedora-i18n/font-rpm-spec-generator)](./LICENSE)

This tool generates RPM [specfile](https://docs.fedoraproject.org/en-US/packaging-guidelines/FontsPolicy/) for a given font.

## setup & use
```
$ pip3 install build
$ python3 -m build
$ pip3 install --user dist/fontrpmspec*.whl
```

## usage

### fontrpmspec-gen
```
usage: fontrpmspec-gen [-h] [-f JSON_FILE] [-l LICENSE] [-o OUTPUT] [--outputdir OUTPUTDIR] [--sourcedir SOURCEDIR]
                       [-s SOURCE] [-u URL] [-c CHANGELOG] [--email EMAIL] [--username USERNAME] [--summary SUMMARY]
                       [--description DESCRIPTION] [-a ALIAS] [--lang [LANG ...]] [--priority PRIORITY]
                       NAME [VERSION]

Fonts RPM spec file generator against guidelines

positional arguments:
  NAME                  Package name
  VERSION               Package version (default: None)

options:
  -h, --help            show this help message and exit
  -f JSON_FILE, --json-file JSON_FILE
                        Config file written in JSON (default: None)
  -l LICENSE, --license LICENSE
                        License name of this project (default: OFL-1.1)
  -o OUTPUT, --output OUTPUT
                        Output file (default: -)
  --outputdir OUTPUTDIR
                        Output directory (default: .)
  --sourcedir SOURCEDIR
                        Source directory (default: .)
  -s SOURCE, --source SOURCE
                        Source file (default: None)
  -u URL, --url URL     Project URL (default: None)
  -c CHANGELOG, --changelog CHANGELOG
                        Changelog entry (default: Initial import)
  --email EMAIL         email address to put into changelog (default: yourname@example.com)
  --username USERNAME   Real user name to put into changelog (default: Your Name)
  --summary SUMMARY     Summary text for package (default: {family}, {alias} typeface {type} font)
  --description DESCRIPTION
                        Package description (default: This package contains {family} which is a {alias} typeface of
                        {type} font.)
  -a ALIAS, --alias ALIAS
                        Set an alias name for family, such as sans-serif, serif, monospace (default: auto)
  --lang [LANG ...]     Targetted language for a font (default: None)
  --priority PRIORITY   Number of Fontconfig config priority (default: 69)
```

### fontrpmspec-conv
```
usage: fontrpmspec-conv [-h] [--sourcedir SOURCEDIR] [-o OUTPUT] SPEC

Fonts RPM spec file converter against guidelines

positional arguments:
  SPEC                  Spec file to convert

options:
  -h, --help            show this help message and exit
  --sourcedir SOURCEDIR
                        Source directory (default: .)
  -o OUTPUT, --output OUTPUT
                        Output file (default: -)
```

Note:
- You may need to update `BuildRequires` section as per your font requiremnts in your spec.
- Also update the `%build` section if your font uses some other build process.

### fontrpmspec-gentmt
```
usage: fontrpmspec-gentmt [-h] [--extra-buildopts EXTRA_BUILDOPTS] [-a] [-O OUTPUTDIR]
                          [-v]
                          REPO

TMT plan generator

positional arguments:
  REPO                  Package repository path

options:
  -h, --help            show this help message and exit
  --extra-buildopts EXTRA_BUILDOPTS
                        Extra buildopts to build package (default: None)
  -a, --add-prepare     Add prepare section for local testing (default: False)
  -O, --outputdir OUTPUTDIR
                        Output directory (default: None)
  -v, --verbose         Show more detailed logs (default: False)
```

Happy Packaging :)
