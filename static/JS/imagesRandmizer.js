function imageRand(){
     // This randomized the images at it shows up
     var images = [ ".../static/images/hiking.jpeg",
                    "../static/images/hiking.jpeg",
                    "../static/images/playing-game.png",
                    "../static/images/monekyEscape.jpeg",
                    "../static/images/expert.jpeg",
                    
    ];
    var i = 0;
    var renew = setInterval(function(){
    if(images.length == i){
        i = 0;
    }
    else {
        document.getElementById("bannerImage").src = images[i]; 
        i++;
    }
    },6000);
}