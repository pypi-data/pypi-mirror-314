# pyasiltags

Uilities to manage ISO26262 safety integrity levels tags

## Description

This microlibrary is meant to be used in tooling where ASIL tags are used, for instance in 
requirements management tooling. ISO26262 mentions the following types of ASIL:

- QM
- ASIL A
- ASIL B
- ASIL C
- ASIL D

In addition the ASIL can be decomposed into lower or equivalent asil using the parenthesis notation:

- QM(y)
- ASIL x(y)

Where x and y can be one of A, B, C, D. Decomposing from QM does not make sense.

The library allows parsing such strings and validating their format, comparing the level between 
`Integrity` objects and checking if a given inheritance of ASIL is valid or not.

## Setup

Simply install the library with `pip`, for instance:

```shell 
python -m pip install pyasiltags
```
