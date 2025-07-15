function setProxyArr(proxyObjArr) {
  for (let i = 0; i < proxyObjArr.length; i++) {
    const objName = proxyObjArr[i];
    const obj = global[objName];

    const handler = {
      get: function(target, property, receiver) {
        console.log("方法:", "get", "对象", objName, "属性:",
          property, "属性类型:", typeof property, "属性值:", target[property], "属性值类型:", typeof target[property]);
        return Reflect.get(...arguments);
      },
      set: function(target, property, value, receiver) {
        console.log("方法:", "set", "对象:", objName, "属性:",
          property, "属性类型:", typeof property, "属性值:", value, "属性值类型:", typeof target[property]);
        return Reflect.set(...arguments);
      }
    };

    global[objName] = new Proxy(obj, handler);
  }
}

window = global
window.Buffer = Buffer

window.constructor = function Window() { }
function HTMLDocument() {

}
HTMLDocument.prototype.creatElement = function(){}
document = new HTMLDocument()
window.Document = HTMLDocument

function Navigator() {

}
Navigator.prototype.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'
navigator = new Navigator()
window.Navigator = Navigator()

function Screen() {

}
screen = new Screen()
window.Screen = Screen

function History() {

}
history = new History()
window.History = History

function Location() {
}
location = new Location()
window.Location = Location

setProxyArr(['document', 'location', 'history', 'screen', 'navigator']);




