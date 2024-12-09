# Humans Library
a Python collection of biblical humans and their family relations

## Quickstart
the library provides different scopes of information

### Father Objects
a set of classes that represent biblical fathers, such as Abraham, Isaac and Jacob.

```
import humans

abraham = humans.Abraham()
print(abraham.__dict__)
```
### List of Humans
on a broader scope, the library traces different categories of humans, such as fathers, mothers and children.
```
import humans

all_mothers = humans.mothers
print(all_mothers)
```