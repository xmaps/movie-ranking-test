

function addMovies(){
	$('#not_voted_movies option:selected').remove().appendTo('#voted_movies');
	$('#voted_movies').attr('size', $('#voted_movies').find('option').length);
	$('#not_voted_movies').attr('size', $('#not_voted_movies').find('option').length);
	return;
}

function removeMovies(){
	$('#voted_movies option:selected').remove().appendTo('#not_voted_movies');
	$('#voted_movies').attr('size', $('#voted_movies').find('option').length);
	$('#not_voted_movies').attr('size', $('#not_voted_movies').find('option').length);
	return;
}

function addAllMovies(){
	$('#not_voted_movies option').remove().appendTo('#voted_movies');
	$('#voted_movies').attr('size', $('#voted_movies').find('option').length);
	$('#not_voted_movies').attr('size', $('#not_voted_movies').find('option').length);
	return;
}

function removeAllMovies(){
	$('#voted_movies option').remove().appendTo('#not_voted_movies');
	$('#voted_movies').attr('size', $('#voted_movies').find('option').length);
	$('#not_voted_movies').attr('size', $('#not_voted_movies').find('option').length);
	return;
}

//On scrolling of DIV tag.
function OnDivScroll(div)
{
    var lstCollegeNames = $(div).find('select');

    //The following two points achieves two things while scrolling
    //a) On horizontal scrolling: To avoid vertical
    //   scroll bar in select box when the size of 
    //   the selectbox is 8 and the count of items
    //   in selectbox is greater than 8.
    //b) On vertical scrolling: To view all the items in selectbox

    //Check if items in selectbox is greater than 8, 
    //if so then making the size of the selectbox to count of
    //items in selectbox,so that vertival scrollbar
    // won't appear in selectbox
    /*if (lstCollegeNames.options.length > 110)
    {
        lstCollegeNames.size=lstCollegeNames.options.length;
    }
    else
    {
        lstCollegeNames.size=110;
    }*/
}
//On focus of Selectbox
function OnSelectFocus(div)
{
    //On focus of Selectbox, making scroll position 
    //of DIV to very left i.e 0 if it is not. The reason behind
    //is, in this scenario we are fixing the size of Selectbox 
    //to 8 and if the size of items in Selecbox is greater than 8 
    //and to implement downarrow key and uparrow key 
    //functionality, the vertical scrollbar in selectbox will
    //be visible if the horizontal scrollbar of DIV is exremely right.
    if ($(div).closest('div').scrollLeft != 0)
    {
        $(div).closest('div').scrollLeft = 0;
    }

    var lstCollegeNames = $(div);
    //Checks if count of items in Selectbox is greater 
    //than 8, if yes then making the size of the selectbox to 8.
    //So that on pressing of downarrow key or uparrowkey, 
    //the selected item should also scroll up or down as expected.
    /*if( lstCollegeNames.options.length > 8)
    {
        lstCollegeNames.focus();
        lstCollegeNames.size=8;
    }*/
}