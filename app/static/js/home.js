// Flixr
// Home Grid JS

var pageNumber = 1;

// Ajax to retrieve movies from server
$(function() {
    $.ajax({
        url: '/getPopularMovies/1',
        type: 'GET',
        success: function(response) {
            var data = JSON.parse(response);
            
            var cardsPerRow = 0;
            var div = $('<div>').attr('class', 'row');
            for (var i = 0; i < data.length; i++) {
                
                // 4 cards per materialize grid row
                if (cardsPerRow < 4) {
                    
                    if (i == data.length - 1) {
                        div.append(CreateCard(data[i].Id, data[i].Title, data[i].Overview, data[i].Poster_Path));
                        $('.cardgrid').append(div);
                    } else {
                        div.append(CreateCard(data[i].Id, data[i].Title, data[i].Overview, data[i].Poster_Path));
                        cardsPerRow++;
                    }
                } else {
                    $('.cardgrid').append(div);
                    div = $('<div>').attr('class', 'row');
                    div.append(CreateCard(data[i].Id, data[i].Title, data[i].Overview, data[i].Poster_Path));
                    if (i == data.length - 1) {
                        $('.cardgrid').append(div);
                    }
                    cardsPerRow = 1;
                }
            }
            pageNumber++;
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// Load more button, onclick function
$('#loadMoreButton').click(function() {
    $.ajax({
        url: '/getPopularMovies/' + pageNumber,
        type: 'GET',
        success: function(response) {
            var data = JSON.parse(response);
            
            var cardsPerRow = 0;
            var div = $('<div>').attr('class', 'row');
            for (var i = 0; i < data.length; i++) {
                
                // 4 cards per materialize grid row
                if (cardsPerRow < 4) {
                    
                    if (i == data.length - 1) {
                        div.append(CreateCard(data[i].Id, data[i].Title, data[i].Overview, data[i].Poster_Path));
                        $('.cardgrid').append(div);
                    } else {
                        div.append(CreateCard(data[i].Id, data[i].Title, data[i].Overview, data[i].Poster_Path));
                        cardsPerRow++;
                    }
                } else {
                    $('.cardgrid').append(div);
                    div = $('<div>').attr('class', 'row');
                    div.append(CreateCard(data[i].Id, data[i].Title, data[i].Overview, data[i].Poster_Path));
                    if (i == data.length - 1) {
                        $('.cardgrid').append(div);
                    }
                    cardsPerRow = 1;
                }
            }
            pageNumber++;
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// View details onclick function
$(document).on('click', '[id^="mov_"]', function() {
    var spId = $(this).attr('id').split('_')[1];
    $.ajax({
        url: '/getMovieDetails/' + spId,
        type: 'GET',
        success: function(response) {
            var data = JSON.parse(response);
            
            // Clear modal of previous content
            $('#modalMovieDetails').empty();
           
            // Append modal content
            $('#modalMovieDetails').append(CreateModal(data.Id, data.Title, data.Overview, data.Rating, data.Release, data.ExistsBookmark));
            
            // Trigger modal
            $('#modalMovieDetails').openModal();   
        }
    });
});

// Bookmark button onclick function
$(document).on('click', '[id^="bBtn_"]', function() {
    var spId = $(this).attr('id').split('_')[1];
    $.ajax({
        url: '/bookmark/' + spId,
        type: 'GET',
        success: function(response) {
            var data = JSON.parse(response);
            if(data.hasOwnProperty('success')) {
                var buttonName = ('#bBtn_' + spId);
                if ($('#bBtn_' + spId).text() == "Bookmark") {
                    ($('#bBtn_' + spId).text("Bookmarked"))
                } else {
                    ($('#bBtn_' + spId).text("Bookmark"))
                }
            } else {
                console.log("Bookmark Failed.");
            }
        },
        error: function(error) {
        console.log(error);
    }
    });
});


// Function to construct a Materialize card
function CreateCard(id, title, overview, ppath) {
    
    var mainDiv = $('<div>').attr('class', 'col s12 m6 l3');
    
    var card = $('<div>').attr('class', 'card hoverable');
    
    var cardimage = $('<div>').attr('class', 'card-image');
    
    var pgrad = $('<div>').attr('class', 'postergrad');
    
    var img = $('<img>').attr({
        'class': 'poster',
        'src': ppath
    });
    
    var cardtitle = $('<span>').attr('class', 'card-title');
    cardtitle.text(title);
    
    var cardcontent = $('<div>').attr('class', 'card-content');
    
    var overviewp = $('<p>').attr('class', 'truncate');
    overviewp.text(overview);
    
    var cardaction = $('<div>').attr('class', 'card-action');
    
    var link = $('<a>').attr({
        'href': '#!',
        'id': 'mov_' + id
    });
    link.text("View Details");
    
    cardaction.append(link);
    cardcontent.append(overviewp);
    pgrad.append(img);
    cardimage.append(pgrad);
    cardimage.append(cardtitle);
    
    card.append(cardimage);
    card.append(cardcontent);
    card.append(cardaction);
    
    mainDiv.append(card);
    return mainDiv;
}


// Function to construct modal contents
function CreateModal(id, title, overview, rating, release, existsBookmark) {
    
    mainDiv = $('<div>').attr('class', 'modalWrapper');
    
    closeBtn = $('<a>').attr({
        'href': '#!',
        'class': 'modal-action modal-close waves-effect waves-green btn-flat'
    });
    closeBtn.text("Close");
    
    if (!existsBookmark) {
        bookmarkBtn = $('<a>').attr({
        'href': '#!',
        'class': 'modal-action waves-effect waves-light btn',
        'id' : 'bBtn_' + id
    });
    bookmarkBtn.text("Bookmark")
    } else {
        bookmarkBtn = $('<a>').attr({
        'href': '#!',
        'class': 'modal-action waves-effect waves-light btn',
        'id' : 'bBtn_' + id
    });
    bookmarkBtn.text("Bookmarked")
    }
    
    var modalFooter = $('<div>').attr('class', 'modal-footer');
    
    var releaseDate = $('<td>').text(release);
    var releaseHeader = $('<td>').text("Release");
    
    var ratingNo = $('<td>').text(rating + "/10.0");
    var ratingHeader = $('<td>').text("Rating");

    var overviewTxt = $('<td>').text(overview);
    var overviewHeader = $('<td>').text("Overview");
    
    var releaseWrapper = $('<tr>');
    var ratingWrapper = $('<tr>');
    var overviewWrapper = $('<tr>');
    
    var tableBody = $('<tbody>');
    var tablewrapper = $('<table>');
    var tableDiv = $('<div>').attr('class', 'col s12');
    var rowDiv = $('<div>').attr('class', 'row');
    
    var movieTitle = $('<h4>').text(title);
    var modalContent = $('<div>').attr('class', 'modal-content');
    
    releaseWrapper.append(releaseHeader);
    releaseWrapper.append(releaseDate);
    
    ratingWrapper.append(ratingHeader);
    ratingWrapper.append(ratingNo);
    
    overviewWrapper.append(overviewHeader);
    overviewWrapper.append(overviewTxt);
    
    tableBody.append(overviewWrapper);
    tableBody.append(ratingWrapper);
    tableBody.append(releaseWrapper);
    
    rowDiv.append(tableDiv.append(tablewrapper.append(tableBody)));
    
    modalContent.append(movieTitle);
    modalContent.append(rowDiv);
    
    modalFooter.append(bookmarkBtn);
    modalFooter.append(closeBtn);
    
    mainDiv.append(modalContent);
    mainDiv.append(modalFooter);
    
    return mainDiv;
}