#API Documentation

##End Points

| End Point     | HTTP Method       | Description | Example |
| :-------------: |:-------------:| :-------------:| :-------------:|
| annotations | GET | Gets a set of annotations. There options are to filter by question id or answer id | /api/annotations?answer_id=3|
| annotations | POST | Creates a new annotation | /api/annotations |
| annotation | GET | Gets a particular annotation based on id | /api/annotation/3 |
| videos | GET  | Gets a set of videos. Can filter by id | /api/videos |
| videos | POST  | Creates a new video. | /api/videos |
| video | GET  | Gets a particular of videos based on id  | /api/video/3 |
| video | PUT  | Gets a set of videos  | /api/video |
| tasks | GET  | Gets a set of tasks  | /api/tasks/ |
| tasks | POST  | Creates a task  | /api/tasks |
| task | GET  | Gets tasks with paritcular id  | /api/task/3 |

Sample data required to create a task:

| Parameter     | Description       | Example  |
| :-------------: |:-------------:| :-------------:|
| question_id     | question of the annotation | 1 |
| answer_id     | answer of the annotation      |   2 |
| keyword | highlighted keyword     |   django internals |
| annotation_url | url to be passed to tweet  | www.stackannotator.com/...  |
