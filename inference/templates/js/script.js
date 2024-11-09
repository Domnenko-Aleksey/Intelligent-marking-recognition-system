window.addEventListener('DOMContentLoaded', function(){
	CORE.init()
});

CORE = {
    content: false,
    input_file: false,
    button_submit: false,

    init(){
        CORE.content = document.getElementById('content');
        CORE.input_file = document.getElementById('input_file');
        CORE.button_submit = document.getElementById('button_submit');
        CORE.input_file.onchange = CORE.display_image;
        CORE.button_submit.onclick = CORE.get_answer;
    },

    display_image(e) {
        var img_files = e.target.files;
        var bg_img = img_files[0];

        var reader = new FileReader();
        reader.onload = function(_src){	
            let img = '<img class="content_img" src="' + _src.target.result + '">';
            CORE.content.innerHTML = img;
        }	
        reader.readAsDataURL(bg_img);
    },

    get_answer(e){
        DAN.modal.spinner();
		let form = new FormData();
		let file = CORE.input_file.files[0];
        form.append('file', file);

		DAN.ajax('/ajax', form, function(data){
			if (data.answer == 'success') {
				DAN.modal.del()
                CORE.content.innerHTML += 
                '<div class="text_wrap">Номенклатура детали:<br><b>' + data.marking + '</b></div>';
			} else {
				alert(data.message)
			}
		})
    }
}