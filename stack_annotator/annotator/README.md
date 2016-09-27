#API Documentation

##End Points
###Annotations
####GET
```
/api/annotations/{id}
```
Gets a set of annotations based on the id. The options are by question id or answer id

Example:
```
/api/annotations?answer_id=3
``` 
Will search for all annotations where the answer_id is 3
```
/api/annotation/{id}
```
Gets a specific annotation with particular id

####POST
```
/api/annotation
```
Posts an annotation

###Tasks
####GET
```
/api/tasks/
```
Returns all tasks

```
/api/task/{id}
```
Gets a specific task with particular id

####POST
```
/api/task
```
Creates a task which also creates the corresponding annotation

Requires the same parameters as an Annotation:

| Parameter     | Description       | Example  |
| :-------------: |:-------------:| :-------------:|
| question_id     | question of the annotation | 1 |
| answer_id     | answer of the annotation      |   2 |
| keyword | highlighted keyword     |   django internals |
| annotation_url | url to be passed to tweet  | www.stackannotator.com/...  |
| position | position of the keyword      |  123  |
