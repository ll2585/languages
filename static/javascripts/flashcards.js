// ref: http://stackoverflow.com/a/1293163/2343
// This will parse a delimited string into an array of
// arrays. The default delimiter is the comma, but this
// can be overriden in the second argument.
function CSVToArray( strData, strDelimiter ){
    // Check to see if the delimiter is defined. If not,
    // then default to comma.
    strDelimiter = (strDelimiter || ",");

    // Create a regular expression to parse the CSV values.
    var objPattern = new RegExp(
        (
            // Delimiters.
            "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +

                // Quoted fields.
            "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +

                // Standard fields.
            "([^\"\\" + strDelimiter + "\\r\\n]*))"
        ),
        "gi"
    );


    // Create an array to hold our data. Give the array
    // a default empty first row.
    var arrData = [[]];

    // Create an array to hold our individual pattern
    // matching groups.
    var arrMatches = null;


    // Keep looping over the regular expression matches
    // until we can no longer find a match.
    while (arrMatches = objPattern.exec( strData )){

        // Get the delimiter that was found.
        var strMatchedDelimiter = arrMatches[ 1 ];

        // Check to see if the given delimiter has a length
        // (is not the start of string) and if it matches
        // field delimiter. If id does not, then we know
        // that this delimiter is a row delimiter.
        if (
            strMatchedDelimiter.length &&
            strMatchedDelimiter !== strDelimiter
        ){

            // Since we have reached a new row of data,
            // add an empty row to our data array.
            arrData.push( [] );

        }

        var strMatchedValue;

        // Now that we have our delimiter out of the way,
        // let's check to see which kind of value we
        // captured (quoted or unquoted).
        if (arrMatches[ 2 ]){

            // We found a quoted value. When we capture
            // this value, unescape any double quotes.
            strMatchedValue = arrMatches[ 2 ].replace(
                new RegExp( "\"\"", "g" ),
                "\""
            );

        } else {

            // We found a non-quoted value.
            strMatchedValue = arrMatches[ 3 ];

        }


        // Now that we have our value string, let's add
        // it to the data array.
        arrData[ arrData.length - 1 ].push( strMatchedValue );
    }

    // Return the parsed data.
    return( arrData );
}

function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex ;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }

    return array;
}

var flashcardApp = angular.module('flashcardApp', []).directive('fileReader', function() {
    return {
        scope: {
            fileReader:"=",
            action: "="
        },
        link: function(scope, element, attrs) {

            $(element).on('change', function(changeEvent) {
                var files = changeEvent.target.files;
                if (files.length) {
                    var r = new FileReader();
                    r.onload = function(e) {
                        var contents = e.target.result;
                        scope.$apply(function () {
                            scope.action(contents);
                        });

                    };

                    r.readAsText(files[0]);
                }
            });

            $(element).on('click', function(){
                $(element).val("")
            })
        }
    };
});


flashcardApp.controller('MainCtrl', ['$scope', '$http', function($scope, $http){
    $scope.message = "HI!";
    $scope.studying = false;
    $scope.cardsSelected = [];
    $scope.keepKnown = false;
    $scope.restartEndString = "RESTART UNKNOWN CARDS";
    $scope.set_size = 8;
    $scope.onCardScreen = true;
    $scope.curCard = 0;
    $scope.showFront = true;
    $scope.nextCardButton = "NEXT CARD";

    $scope.openFile = function(){
        console.log("CLICKED")
        var r = new FileReader();
        r.onload = function(e) {
            var contents = e.target.result;
            $scope.loadCSV(contents);

        };
    };
    $scope.loadCSV = function(contents){
        $scope.fileContents = contents;
        $scope.data = contents.split(/\r?\n/);
        $scope.cards = [];
        for(var i = 0; i < $scope.data.length; i++){
            $scope.cards.push($scope.data[i].split(/\t/));
            $scope.cardsSelected.push(false);
        }
        console.log($scope.cards);
    };

    $scope.generateRandomID = function(){
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for( var i=0; i < 10; i++ ){
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        }

        return text;
    };
    $scope.start = function(){
        $scope.toReview = [];
        $scope.reviewingSet = [];
        $scope.cardKnown = [];
        for(var i = 0; i < $scope.cardsSelected.length; i++){
            if($scope.cardsSelected[i]){
                $scope.toReview.push($scope.cards[i]);
                $scope.reviewingSet.push($scope.cards[i]);
                $scope.cardKnown.push(false);
            }
        }
        shuffle($scope.toReview);
        shuffle($scope.reviewingSet);
        $scope.studying = true;
        $scope.onCardScreen = true;
        $scope.curCard = 0;
        $scope.showFront = true;
        $scope.updateCard();
        $scope.nextCardButton = "NEXT CARD";
    };

    $scope.noCardsSelected = function(){
        for(var i = 0; i < $scope.cardsSelected.length; i++){
            if($scope.cardsSelected[i]){
                return false;;
            }
        }
        return true;
    };

    $scope.getCardIndex = function(curIndex){
        if ($scope.reviewingSet != null) {
            var curCardFront = $scope.reviewingSet[curIndex][0];
            for (var i = 0; i < $scope.cards.length; i++) {
                if ($scope.cards[i][0] == curCardFront) {
                    return i;
                }
            }
        }
    }

    $scope.startAll = function(){
        $scope.toReview = [];
        $scope.reviewingSet = [];
        $scope.cardKnown = [];
        for(var i = 0; i < $scope.cards.length; i++){
                $scope.toReview.push($scope.cards[i]);
                $scope.reviewingSet.push($scope.cards[i]);
                $scope.cardKnown.push(false);
        }
        shuffle($scope.toReview);
        shuffle($scope.reviewingSet);
        $scope.studying = true;
        $scope.onCardScreen = true;
        $scope.curCard = 0;
        $scope.showFront = true;
        $scope.updateCard();
        $scope.nextCardButton = "NEXT CARD";
    };

    $scope.shuffleCards = function(){
        var checkedDict = {};
        for(var i = 0; i < $scope.cards.length; i++){
            checkedDict[$scope.cards[i][0]] = $scope.cardsSelected[i];
        }
        shuffle($scope.cards);
        for(var i = 0; i < $scope.cards.length; i++){
            $scope.cardsSelected[i] = checkedDict[$scope.cards[i][0]];
        }
    };

    $scope.restartUnknown = function(){
        //change to $scope.start when live...
        var temp = [];
        for(var i = 0; i < $scope.cardKnown.length; i++){
            if(!$scope.cardKnown[i]){
                temp.push($scope.reviewingSet[i]);
            }
        }
        $scope.reviewingSet = temp;
        $scope.cardKnown = [];
        for(var i = 0; i < $scope.reviewingSet.length; i++){
            $scope.cardKnown.push(false);
        }

        shuffle($scope.reviewingSet);
        $scope.studying = true;
        $scope.onCardScreen = true;
        $scope.curCard = 0;
        $scope.showFront = true;
        $scope.nextCardButton = "NEXT CARD";
        $scope.updateCard();

    };

    $scope.restartIncludingKnown = function(){
        //change to $scope.start when live...
        $scope.reviewingSet = [];
        $scope.cardKnown = [];
        for(var i = 0; i < $scope.toReview.length; i++){
            $scope.reviewingSet.push($scope.toReview[i])
            $scope.cardKnown.push(false);
        }

        shuffle($scope.reviewingSet);
        $scope.studying = true;
        $scope.onCardScreen = true;
        $scope.curCard = 0;
        $scope.showFront = true;
        $scope.updateCard();
        $scope.nextCardButton = "NEXT CARD";
    };

    $scope.restartEndScreen = function(){
        if($scope.keepKnown){
            $scope.restartIncludingKnown();
        }else{
            $scope.restartUnknown();
        }
    };

    $scope.restartThisSet = function(){
        $scope.cardKnown = [];
        for(var i = 0; i < $scope.reviewingSet.length; i++){
            $scope.cardKnown.push(false);
        }

        shuffle($scope.reviewingSet);
        $scope.studying = true;
        $scope.onCardScreen = true;
        $scope.curCard = 0;
        $scope.showFront = true;
        $scope.nextCardButton = "NEXT CARD";
        $scope.updateCard();
    };




    $scope.toggleKeep = function(){
        $scope.restartEndString = $scope.keepKnown ? "RESTART THIS SET INCLUDING KNOWN" : "RESTART UNKNOWN CARDS";
    };

    $scope.nextCard = function(){
        if($scope.curCard == $scope.reviewingSet.length-1){
            $scope.knownCards = 0;
            for(var i = 0; i < $scope.cardKnown.length; i++){
                if($scope.cardKnown[i]){
                    $scope.knownCards += 1;
                }
            }
            $scope.keepKnown = false;
            $scope.toggleKeep();
            $scope.onCardScreen = false;
        }else{
            $scope.curCard += 1;
            $scope.showFront = true;
            if($scope.curCard == $scope.reviewingSet.length-1){
                $scope.nextCardButton = "TO RESULTS!"
            }else{
                $scope.nextCardButton = "NEXT CARD"
            }

        }
        $scope.updateCard();
    };

    $scope.prevCard = function(){
        if($scope.curCard == 0){

        }else{
            $scope.curCard -= 1;
            $scope.showFront = true;
        }
        $scope.updateCard();
    };

    $scope.flipCard = function(){
        console.log("??");
        $scope.showFront = !$scope.showFront;
        $scope.updateCard();
    };

    $scope.knowCard = function(){
        $scope.cardKnown[$scope.curCard] = !$scope.cardKnown[$scope.curCard];
        $scope.updateCard();
    };


    $scope.updateCard = function(){
        $scope.curSide = $scope.reviewingSet[$scope.curCard][$scope.showFront ? 0 : 1];
        if($scope.curCard == $scope.reviewingSet.length-1){
            $scope.nextCardButton = "TO RESULTS!"
        }else{
            $scope.nextCardButton = "NEXT CARD"
        }
    };

    $scope.getRange = function(){
        if($scope.cards) {
            var result = {};
            var card_length = $scope.cards.length;

            for (var i = 0; i < card_length / $scope.set_size; i++) {
                result[i] = (i * $scope.set_size) + " to " + Math.min(card_length - 1, ((i + 1) * $scope.set_size - 1));
            }
            return result;
        }
    };
    $scope.startSet = function(value){
        $scope.toReview = [];
        $scope.reviewingSet = [];
        $scope.cardKnown = [];
        var card_length = $scope.cards.length;
        for(var i =(value * $scope.set_size); i < Math.min(card_length - 1, ((value*1 + 1) * $scope.set_size - 1))+1; i++){
            $scope.toReview.push($scope.cards[i]);
            $scope.reviewingSet.push($scope.cards[i]);
            $scope.cardKnown.push(false);
        }
        shuffle($scope.toReview);
        shuffle($scope.reviewingSet);
        $scope.studying = true;
        $scope.onCardScreen = true;
        $scope.curCard = 0;
        $scope.showFront = true;
        $scope.updateCard();
        $scope.nextCardButton = "NEXT CARD";

    };

    $scope.end = function(){
        $scope.studying = false;
    };
    $scope.checkCardForReview = function(){
        $scope.cardsSelected[$scope.getCardIndex($scope.curCard)] = !$scope.cardsSelected[$scope.getCardIndex($scope.curCard)];
    }
    $scope.randomID = $scope.generateRandomID();

    $scope.key = function($event){
        if($scope.studying) {
            if(!$scope.onCardScreen){
                if ($event.keyCode == 39) {//("right arrow");
                    if(!(!$scope.keepKnown && $scope.knownCards == $scope.reviewingSet.length)){
                        $scope.restartEndScreen();
                    }

                }else if ($event.keyCode == 32) { //("space");

                    $scope.keepKnown = !$scope.keepKnown;
                    $scope.toggleKeep();
                }
                else if ($event.keyCode == 13) { //("enter");
                    $scope.end();
                }
            }else {
                console.log($event.keyCode);
                if ($event.keyCode == 38) { //("up arrow");
                    $scope.flipCard();
                }
                else if ($event.keyCode == 39) {//("right arrow");
                    $scope.nextCard();
                }
                else if ($event.keyCode == 40) { //("down arrow");
                    $scope.flipCard();

                }
                else if ($event.keyCode == 37) { //("left arrow");
                    $scope.prevCard();
                }
                else if ($event.keyCode == 32) { //("space");
                    $scope.knowCard();
                }
                else if ($event.keyCode == 13) { //("enter");
                    $scope.end();
                }
                else if ($event.keyCode == 67) { //("c");
                    $scope.checkCardForReview();
                }
            }
        } else{
            if ($event.keyCode > 48 && $event.keyCode <58 ) { //("1 to 9");
                $scope.startSet($event.keyCode-49);
            }
            else if ($event.keyCode == 83) { //("s");
                $scope.shuffleCards();
            }

        }
    }

}]);