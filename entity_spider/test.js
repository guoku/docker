Person = function () {
    this.name = 'a';
    this.run = function(){
        console.log('running');
    }
}


p1 = new Person();
p1.run()


Cat = function(){
    var a = new Object();
    a.name = 'miao';
    a.run = function(){
        console.log('cat runnig');
    }
}


var myCat = Cat();
myCat.run();


function go(){
    var a = 'guoku';
    var b =  function(){
        console.log(a);
    }

    return b ;
}

x = go();

$('li').click(function(event){
    var id = event.currentTarget.id;
    console.log(id);
})

