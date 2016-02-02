paceOptions = {
    ajax: false, // disabled
    document: false, // disabled
    eventLag: false, // disabled
    elements: {
        selectors: ['.gk7-douban-send-end']
    }
};
document.addEventListener('DOMContentLoaded', function () {
    
    chrome.extension.sendMessage('id',{'sa':'12312'}, function (response){
	
    });
});

$(document).ready(function (){
    $('.menu .item').click(function (){
	if ($(this).hasClass('active')){
	    return;
	}
	$('.menu').find('.item').each(function (){
	    $(this).removeClass('active');
	});
	$(this).addClass('active');
	var tab = $('div').find('div[data-tab="' + $(this).attr('data-tab') + '"]');
	$('.tab').css('display', 'none');
	tab.css('display', 'block');
    });

});
