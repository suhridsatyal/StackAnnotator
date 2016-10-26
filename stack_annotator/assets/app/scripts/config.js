define([], function() {

    var Config = {
        stackoverflow: {
            url_root:'https://api.stackexchange.com/2.2/questions/',
            question_query: '?order=desc&sort=activity&site=stackoverflow&filter=withbody',
            answer_query: '/answers?order=desc&sort=activity&site=stackoverflow&filter=withbody',
            key: '' //provide a key if you want to access more than 300 stackOverflow requests per day
        },
        stackannotator: {
            url_root: 'http://stackannotator.com',
            api_url_root: 'http://stackannotator.com/api',
            videos_endpoint: '/videos',
            video_endpoint: '/video',
            tasks_endpoint: '/tasks',
            annotation_endpoint: '/annotation',
            annotations_endpoint: '/annotations',
        }
    };

    return Config;
});
