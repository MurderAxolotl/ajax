### JSON Patch Definitions

JSON patch definitions are the simplier way of creating a patch. They're ideal for when you just need to replace or insert text.

### Getting Started

To get started, check the [template](https://github.com/psychon-night/ajax/blob/main/templates/json_patch.json). This shows you all available fields and gives a basic example of how to use it.

Here's a quick breakdown of each key:

| Key       | Acceptable Values | Description                         |
|-----------|-------------------|-------------------------------------|
| patchName | Any string        | The name of the patch               |
| patchAuth | Any string        | The patch's author                  |
| patchDesc | Any string        | Description of patch                |
| needsGlbs | true / false      | Whether global patches are required |
| rules     | array of objects  | Contains the patch rules            |

Here's each key of a `rules` object:

| Key      | Acceptable Values                          | Description                       |
|----------|--------------------------------------------|-----------------------------------|
| file     | Any string                                 | The file to edit                  |
| ruleName | Any string                                 | Name of the rule                  |
| ruleType | "REPLACE"<br>"INSERT_AFTER"<br>"INSERT_BEFORE" | What to do when a match is found  |
| search   | Any string                                 | The text to search for            |
| inject   | Any string                                 | The text to replace with / insert |
