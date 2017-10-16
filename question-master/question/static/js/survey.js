(function (window, $) {

    var _cur_page = 0;
    
    
        $('.survey-option').on('click', function () {
            var el = $(this);
            //alert($("#type").val());
            if($("#type").val()==0){//单选
            	$('.survey-option').removeClass('survey-select');
            	el.addClass('survey-select');
            }else {//多选
            	//alert(el.hasClass("survey-select"));
            	if(el.hasClass("survey-select")){
            		el.removeClass('survey-select');//修改答案
            	}else{
            		el.addClass('survey-select');//选择答案
            	}
            	
            }
           
            var idx = $('.survey-select').index();
        });
  

  
   

    $('#next,#over').on('click', function () {
        if (0 == $('.survey-select').length) {
            alert('请选择答案');
            return;
        }
        var answer = "";
        
        $(".survey-select").each(function(i){ 
        	//console.log(this);
        	answer = answer + $(this).attr('id').substring(4);
        });
        
        
        //var answer = $('.survey-select').attr('id').substring(4);
        //alert(answer);
        $("#answer").val(answer);
        $("#fm").submit();
       
    });



    

    
}(window, jQuery));

function btnSubmit(){
    $("#fm").attr('action','/answer/commit');
}