---
date: 2013-06-26
categories:
  - Java
  - XML
share: assets/social/json-schema-to-xsd.png
description: "Everyone is moving from XML to JSON. I just wrote a tool that goes the other way."
---

# JSON Schema to XSD

Everyone is moving from XML to JSON. I just wrote a tool that goes the other way.

<!-- more -->

I am not nostalgic about XML. But a lot of systems still describe their services with an XML schema, also when the payloads themselves are JSON. So you end up with one definition in JSON Schema, and the need for the same thing as XSD on the other side. Writing both by hand means they will drift apart, and you find out when a message is rejected.

So I generate one from the other. [jsons2xsd](https://github.com/ethlo/jsons2xsd) takes a JSON Schema and gives you an XSD.

```java
final Config cfg = new Config.Builder()
    .targetNamespace("http://example.com/myschema.xsd")
    .name("array")
    .build();
final Document doc = Jsons2Xsd.convert(reader, cfg);
```

A property like this:

```json
"name": {
  "type": "string",
  "minLength": 5,
  "maxLength": 32
}
```

becomes this:

```xml
<element name="name">
  <simpleType>
    <restriction base="string">
      <minLength value="5" />
      <maxLength value="32" />
    </restriction>
  </simpleType>
</element>
```

Required properties become plain elements, and optional ones get `minOccurs="0"`. `date-time` becomes `dateTime`, and `number` becomes `decimal`.

That was the easy part. The two do not think alike. JSON Schema says what a value may be. XSD says what a document looks like, in order. A JSON number has no size, and XSD wants to know if it is an `int` or a `long`. Arrays are natural in one and a repeated element in the other. Not everything survives the trip, and I have only done the parts I need.

*Update, November 2026: it became my most starred repository. The issues over the years were about what I guessed in 2013: arrays, simple types and int64.*
