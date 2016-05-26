(function () {
    document.cmd = '';
    document.bbd = '';
    var dic = {};
    function getJsonCallback(json) {
        var result = json.data.result;
        var data = { name: result.name, id: result.mid, url: result.mpath[2] };
        //var cmd = 'wget -O "' + dic[data.id] + " - " + data.name + '.mp4" ' + data.url;
        var cmd = data.url
        var bbd = "'" + dic[data.id] + ' - ' + data.name + "',";
        console.log(dic[data.id] + ' - ' + data.name);
        document.cmd += cmd;
        document.cmd += '\r\n';
        document.bbd += bbd;
        document.bbd += '\r\n';
    }

    var index = 1;
    $('.J-media-item').each(function () {
        var url = $(this).attr('href');
        console.log(url);
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
