# KvCommon-Flask

Library of various [Flask](https://flask.palletsprojects.com/en/3.0.x/) utils that aren't worthy of their own dedicated libs.

This library isn't likely to be useful to anyone else; it's just a convenience to save me from copy/pasting between various projects I work on.

# PyPi
https://pypi.org/project/kvcommon-flask/

# Installation
### With Poetry:
`poetry add kvcommon-flask`

### With pip:
`pip install kvcommon-flask`

## Packages/Modules

| Package | Description |
|---|---|
|`context`|Convenience utils for manipulating Flask config and flask.g context
|`headers`|Utils for manipulating request/response headers and converting them from different formats for use with Flask
|`metrics`|Prometheus Metrics utils & boilerplate
|`middleware`|Basic middleware class using flask-http-middleware with prometheus metrics
|`responses`|Utils and classes for common HTTP Responses with built-in prometheus metrics
|`scheduler`|Utils for scheduling jobs on cron-like intervals with Flask-APScheduler and metrics + logging
|`traces`|OTLP Traces utils & boilerplate
