function filterClass(jsonObject){
    var course_and_class_dict = JSON.parse(jsonObject);
    var course_select = document.getElementById('id_course');
    var class_select = document.getElementById('id_clazz');
    var i;
    for(i = 0; i < course_select.length; i++){
        if(course_select[i].selected){
            class_set = course_and_class_dict[course_select[i].text]
        }
    }
    for(i = 0; i < class_select.length; i++){
        if(class_set.indexOf(class_select[i].text) === -1){
            class_select[i].style.display = "none";
        }
        else{
            class_select[i].style.display = "";
        }
    }
}
