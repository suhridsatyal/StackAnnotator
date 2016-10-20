define([], function() {

    var Config = {
        stackoverflow: {
            url_root:'https://api.stackexchange.com/2.2/questions/',
            question_query: '?order=desc&sort=activity&site=stackoverflow&filter=withbody',
            answer_query: '/answers?order=desc&sort=activity&site=stackoverflow&filter=withbody',
            //key: '' //provide a key if you want to access more than 300 stackOverflow requests per day
        },
        stackannotator: {
            url_root: 'http://stackannotator.com',
            api_url_root: 'http://stackannotator.com/api',
            video_post_endpoint: '/videos',
            video_get_endpoint: '/video',
            video_increment_resource_endpoint: '/video',    
            task_post_endpoint: '/tasks',   
            annotation_post_endpoint: '/annotations'
        },
        regex: {
            stackoverflow: '^(https?:\/\/)?stackoverflow\.com\/questions\/([0-9]+)(\/[-a-z\d%_.~+]*)*',
            youtube: /^https?\:\/\/www\.youtube\.com\/watch\?v\=([\w-]+)(?:&t=(\w+))?$/g
        },
        keyboard_codes: {
            enter: 13
        }
    };

    return Config;
});