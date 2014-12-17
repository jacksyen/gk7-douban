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
