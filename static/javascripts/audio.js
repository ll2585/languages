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

var audioApp = angular.module('audioApp', []).directive('audios', function($sce) {
    return {
        restrict: 'A',
        scope: { code:'=' },
        replace: true,
        template: '<audio ng-src="{{url}}" controls></audio>',
        link: function (scope) {
            scope.$watch('code', function (newVal, oldVal) {
                if (newVal !== undefined) {
                    console.log(newVal);
                    scope.url = $sce.trustAsResourceUrl(newVal['url']);
                }
            });
        }
    };
}).directive('fileReader', function() {
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
                            scope.action(files[0]);
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
zip.workerScriptsPath = "static/javascripts/lib/";
audioApp.controller('MainCtrl', ['$scope', '$http', function($scope, $http){
    $scope.message = "HI!";
    $scope.selectedGame = '';
    $scope.selectedGameURL = null;

    $scope.loadZip = function(contents){
        $scope.filenameBlobDict = {};
        $scope.entries = [];
        zip.createReader(new zip.BlobReader(contents), function(reader) {
          // get all entries from the zip
          reader.getEntries(function(entries) {
            if (entries.length) {
                for(var i = 0; i < entries.length; i++){
                    var entry = entries[i];
                    $scope.entries.push(entry);
                    var filename = entry.filename;
                    if(filename.slice(-3) == 'tsv'){
                       entry.getData(new zip.TextWriter(), function(text) {
                           $scope.loadTSV(text);
                           $scope.$apply();
                        });
                    }else{
                        $scope.loadEntry(entry);
                    }
                }
            }
          });
        });
    };

    $scope.loadEntry = function(entry){
        var fileName = entry.filename.split('/')[1];
        if(fileName.slice(-3) == 'mp3') {
            entry.getData(new zip.BlobWriter(), function (blob) {
                var blobURL = URL.createObjectURL(blob);
                $scope.filenameBlobDict[entry.filename.split('/')[1]] = blobURL;
                if (!(fileName in $scope.audios)) {
                    $scope.audios[entry.filename.split('/')[1]] = {"show": false};
                }
                $scope.audios[entry.filename.split('/')[1]]['url'] = blobURL;
            });
        }
    };
    $scope.generateRandomID = function(){
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for( var i=0; i < 10; i++ ){
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        }

        return text;
    };

    $scope.randomID = $scope.generateRandomID();

    $scope.audios = {

    };


    $scope.audioIndex = {};

    $scope.show = function(audio){
        audio['show'] = !audio['show'];
    };

    $scope.download = function(audio){
        console.log(audio['url']);
    };

    $scope.speed = 100;

    $scope.set_speed = function(speed) {
        for(var s in $scope.audios){
            var vid = document.getElementById(s);
            vid.playbackRate = speed/100;
        }
    };
    $scope.status="RED";
    $scope.loadTSV = function(contents){
        $scope.data = contents.split(/\r?\n/);
        $scope.status="BS";
        $scope.lines = [];
        for(var i = 0; i < $scope.data.length; i++){
            $scope.lines.push($scope.data[i].split(/\t/));
        }
        for(var i = 0; i < $scope.lines.length; i++){
            var mp3_text = $scope.lines[i][2].split(':')[1].slice(0,-1);
            if (!(mp3_text in $scope.audios)){
                $scope.audios[mp3_text] = {"show": false};
            }
            $scope.audios[mp3_text]['transcription'] = $scope.lines[i][3];
        }
    };

}]);