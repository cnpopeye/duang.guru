
function show(info,tab){
    $.ajax({
        url:info.pageUrl,
        type:"GET",
        dataType: "html",
        async:false,
        timeout: 1e4,
        success:function(data){
            var htmltext = "";
            $(data).find('p').each(function(){
                htmltext += $(this).text().replace(/(\n)+|(\r\n)+|(\s)+/g,"")
            })
            $(data).find('h1').each(function(){
                htmltext += $(this).text().replace(/(\n)+|(\r\n)+|(\s)+/g,"")+"\n"
            })
            $(data).find('h2').each(function(){
                htmltext += $(this).text().replace(/(\n)+|(\r\n)+|(\s)+/g,"")+"\n"
            })
            // $(data).find('div').each(function(){
            //     htmltext += $(this).text().replace(/(\n)+|(\r\n)+|(\s)+/g,"")
            // })
            // $(data).find('span').each(function(){
            //     htmltext += $(this).text().replace(/(\n)+|(\r\n)+|(\s)+/g,"")
            // })
            var selectStr = info.selectionText.replace(/(\n)+|(\r\n)+|(\s)+/g,"");
            var str = ".{0,50}"+selectStr+".{0,50}";
            var resultreg = new RegExp(str,"g");
            var result = resultreg.exec(htmltext);
            var msg = String(result).replace(selectStr,">>>"+selectStr+"<<<");
            OpenWindow=window.open("", "newwin", "height=250, width=450,toolbar=no,scrollbars=no,menubar=no");
            OpenWindow.document.write("<HTML>")
            OpenWindow.document.write("<TITLE>例子</TITLE>")
            OpenWindow.document.write("<script>")
            OpenWindow.document.write("function returnValue(){var msg = document.getElementById('text').value;")
            OpenWindow.document.write("var title=document.getElementById('title').value;var url=document.getElementById('url').value;var comment=document.getElementById('comment').value;")
            OpenWindow.document.write("var params = {text:msg,title:title,url:url,comment:comment};params=JSON.stringify(params);")
            OpenWindow.document.write("var xmlhttp=new XMLHttpRequest();xmlhttp.open('POST','http://api.duang.guru/duang',false);")
            OpenWindow.document.write("xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');")
            OpenWindow.document.write("xmlhttp.setRequestHeader('Content-length', params.length);")
            OpenWindow.document.write("xmlhttp.setRequestHeader('Connection', 'close');xmlhttp.send(params);window.close()}")
            OpenWindow.document.write("</script>")
            OpenWindow.document.write("<BODY>")
            OpenWindow.document.write("<textarea id='title' hidden=true>"+tab.title+"</textarea>")
            OpenWindow.document.write("<textarea id='url' hidden=true>"+info.pageUrl+"</textarea>")
            OpenWindow.document.write("内容")
            OpenWindow.document.write("<textarea id='text' rows='10'>"+msg+"</textarea>")
            OpenWindow.document.write("评论")
            OpenWindow.document.write("<textarea id='comment' rows='10'></textarea>")
            OpenWindow.document.write("<button onClick=window.close()>close</button>")
            OpenWindow.document.write("<button onClick=returnValue()>send</button>")
            // OpenWindow.document.write("<textarea rows='5'>"+str+"</textarea>")
            // OpenWindow.document.write("<textarea rows='50' cols = 50>"+htmltext+"</textarea>")
            OpenWindow.document.write("</BODY>")
            OpenWindow.document.write("</HTML>")
                
        },

        error:function(msg) {
            alert('error');
        }
    });
}  

var searchItem = chrome.contextMenus.create({"title": "发送错误消息", "contexts":["selection"], "onclick": show});
