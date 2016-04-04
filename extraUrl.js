(function () {
    document.cmd = '';
    var dic = {};
    function getJsonCallback(json) {
        var result = json.data.result;
        var data = { name: result.name, id: result.mid, url: result.mpath[0] };
        var cmd = 'wget -O "' + dic[data.id] + " - " + data.name + '.mp4" ' + data.url;
        console.log(cmd);
        document.cmd += cmd;
        document.cmd += '\r\n';
    }

    var index = 1;
    $('.J-media-item').each(function () {
        var url = $(this).attr('href');
        var data = url.split('/');
        var type = data[1];
        var id = data[2];
        if(type != 'video'){
            return;
        }

        var jsonPath = "http://www.imooc.com/course/ajaxmediainfo/?mid=" + id + "&mode=flash";
        dic[id] = index;
        $.getJSON(jsonPath, getJsonCallback);
        index++;
    });
})();
