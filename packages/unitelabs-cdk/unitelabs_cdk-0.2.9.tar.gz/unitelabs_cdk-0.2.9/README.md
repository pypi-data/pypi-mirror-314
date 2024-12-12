# UniteLabs Connector Framework

The UniteLabs Connector Framework is a free and open-source framework that enables you to build connectors for
laboratory hard- and software systems with interfaces that are based on industry standards like
[SiLA 2](https://sila-standard.com). If you plan on implementing an interface natively for your device or as wrapper
around an existing proprietary interface, you can use this framework to get it built quickly without deep-diving into
the standard specifications with our intuitive, code-first approach. It provides configurable modules you can use to
quickly integrate the hardware or software you want to connect.

## Installation

[<img src="https://img.shields.io/badge/python-≥3.9.2-0052FF.svg?logo=LOGO&amp;labelColor=090422">](LINK)
[<img src="https://img.shields.io/badge/poetry-≥1.3.1-0052FF.svg?logo=LOGO&amp;labelColor=090422">](LINK)

The UniteLabs Connector Framework requires Python 3.9 or later. To get started quickly, we recommend to clone one of the
starter projects with:

```
$ git clone --depth 1 https://gitlab.com/unitelabs/connector-starter.git <my-connector-name>
$ cd <my-connector-name>
$ poetry install
$ poetry run connector start
```

You can also manually create a new project from scratch and [install the framework](docs/1.get-started/2.installation.md)
with pip. In this case, of course, you'll be responsible for creating the project boilerplate files yourself.

```
$ pip install unitelabs-connector-framework
```

## Documentation

Explor the UniteLabs [Connector Development Kit documentation](https://docs-unitelabs-web-815d69b03b66df4c3a4817af38d7e7b09a17f7c4b50b.gitlab.io/connectivity/overview) 
on our docs page. From there you can find your way to the tutorials and guides.

## Contribute

There are many ways to contribute to this project and our vision of freely and readily available interfaces for laboratory systems.

- Check out our [contribution guidelines](docs/6.community/1.contributing.md) to help us improve this project
- Join the over 400 developers in the [SiLA Slack community](https://sila-standard.org/slack)
- Give back to the community and add your connectors to the [UniteHub](https://hub.unitelabs.io) by sending us an
  [email](mailto:connectors@unitelabs.io)!
- Get in touch with our developers regarding feedback and feature requests at [developers@unitelabs.io](mailto:developers@unitelabs.io)
- Give us a ⭐️ on [GitLab](https://gitlab.com/unitelabs/dev-tools/python-cdk)

## License

We, UniteLabs, provide and maintain this free and open-source framework with the aim to enable the community to overcome
any barriers in digitalizing their laboratory environment. We highly appreciate, if the users of this framework value
the same principles. Therefore, if you want to make your connectors available for others, we encourage you to share them
on our sharing platform, the [UniteHub](https://hub.unitelabs.io). As we do not want to enforce disclosure of your work,
we distribute this framework under the [MIT license](LICENSE).
