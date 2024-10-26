# Architecture Decision Record (ADR)

## Title: Further Refinements to the Gilded Rose After the Initial Refactor

### Status
Proposed

### Context
The `GildedRose` class in file `python/gilded_rose.py` is responsible for updating the quality and sell in value of various items in a store based on specific rules. Currently, the rules are defined within the `update_quality` method, leading to a tightly coupled design. This makes it hard to extend or update the rules without modifying the method itself. Additionally, the inference of item types based on substring matches in the item names may lead to potential errors if item names are not well-defined, ambiguous or contains multiple substring matches.

### Decision
To improve the maintainability and clarity of the code, I propose the following changes:

1. **Modularisation of Rules**: Move the `rules` dictionary to a separate module. This change will allow for better organisation of code and separation of concerns. By passing the specific module containing the rules dictionary as a keyword argument in the `GildedRose` class's initialisation (`__init__`) method, we enable the flexibility to change rules dynamically without modifying the class itself.

2. **Refactoring Item Class Structure**: Introduce a `type` attribute to the `Item` class. This attribute will allow each item to explicitly define its type, making it easier to apply specific required rules. The type will no longer be inferred based on substring matches of the item name, which can lead to potential issues. Rather, the item type should be explicitly defined upon initialisation.

### Consequences
- **Benefits**:
  - Allow for other process with different rules to use class.
  - Improved separation will lead to the codebase being easier to navigate and maintain.
  - Greater flexibility when introducing new item types, modifying existing rules or creating new rules.
  - Explicitly defining the item type reduces the chance of misclassifying items, this will lead to more stable behavior.

- **Risks**:
  - Temporary disruptions during the transition (if the code was in production). This is because refactoring will require updates to any existing code that may be in use.
  - Care must be taken to ensure any part of the system that replies on this has been updated to include the new item attribute and take use of the modularisation of rules.

### Next Steps
- Create a separate module for the rules dictionary and update the `GildedRose` class to accept a module reference as a keyword argument.
- Refactor the `Item` class to include a `type` attribute.
- Rigorously test implementation to confirm that existing functionality is still operable and that the new code base is working as expected.

### References
- Current codebase of the `GildedRose` class and `Item` class.
- [Decision record template by Jeff Tyree and Art Akerman](https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-by-jeff-tyree-and-art-akerman).