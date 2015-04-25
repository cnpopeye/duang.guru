
var db = connect("localhost:27017/duang_guru");


//add versions
db.duang.drop();

db.duang.insert([
{
	title:"这是标题".toString("utf8"),
	host_name:"www.a.com",
	url:"http://www.a.com/adsf.html",
	text:"内容有误，这是>>>错<<<别字".toString("utf8"),
	comment:"因该是：错别字".toString("utf8"),
	created_at:new Date(),
	verify_at:new Date(),
	verify:true,
	ip_address:"112.32.32.41",
	sent_at:NumberInt(-1),
	user_agent:"user-agent"
},
{
	title:"这是标题".toString("utf8"),
	host_name:"www.b.com",
	url:"http://www.b.com/adsf.html",
	text:"内容有误，这是>>>错<<<别字".toString("utf8"),
	comment:"因该是：错别字".toString("utf8"),
	created_at:new Date(),
	verify_at:new Date(),
	verify:true,
	ip_address:"112.32.32.41",
	sent_at:NumberInt(-1),
	user_agent:"user-agent"
},
{
	title:"这是标题".toString("utf8"),
	host_name:"www.a.com",
	url:"http://www.a.com/adsf.html",
	text:"内容有误，这是>>>错<<<别字".toString("utf8"),
	comment:"因该是：错别字".toString("utf8"),
	created_at:new Date(),
	verify_at:new Date(),
	verify:true,
	ip_address:"112.32.32.41",
	sent_at:NumberInt(-1),
	user_agent:"user-agent"
}
]);



db.source.drop();

db.source.insert([
{
	name:"某A网".toString("utf8"),
website:"www.a.com",
support_email:"99504183@qq.com"
},
{
	name:"某B网".toString("utf8"),
website:"www.b.com",
support_email:"99504183@qq.com"
}
]);

