define([], function() {
    return {
        stackoverflow: {
            url_root:'https://api.stackexchange.com/2.2/questions/',
            question_query: '?order=desc&sort=activity&site=stackoverflow&filter=withbody&key=',
            answer_query: '/answers?order=desc&sort=activity&site=stackoverflow&filter=withbody&key=',
            key: 'L30zaZ1PnRBr57w8wAxBMQ(('
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
        }
    };
});