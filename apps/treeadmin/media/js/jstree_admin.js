$(document).ready(function() {
    $.ajaxSetup({
        cache: false,
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", $(":hidden[name=csrfmiddlewaretoken]:eq(0)").val());
            }
        }
    });
	$("#tree").css('background-color', '#fff')
    $("#tree")
	.bind("loaded.jstree", function (e, data) {
        $("li.jstree-closed").each(function(i){
            data.inst.open_node($(this));
        });
	})
	.jstree({
        core: {
            animation: 0
        },
        plugins: [ "themes", "html_data", "dnd", "crrm", "contextmenu" ],
		themes : {
            theme : "default",
            dots : true,
            icons : true
        },
        contextmenu: {
            items: {
                ccp: false,
                create: {
                    label: "Создать",
                    action: function (obj) {
                        this.create(obj);
                    }
                },
                rename: {
                    label: "Переименовать",
                    action: function (obj) {
                        this.rename(obj);
                    }
                },
				hide: {
                    label: "Скрыть/показать",
                    action: function (obj) {
						var url = 'hide/';
						if (obj.hasClass('HiddenNode')) {
							url = 'show/';
						}
						$.ajax({
							async : false,
							type: 'POST',
							url: url,
							data : { 
								"node" : obj.attr("id").replace("n","")
							},
							success: function(){
								if (url == 'show/') {
									obj.removeClass('HiddenNode');
								}
								if (url == 'hide/') {
									obj.addClass('HiddenNode');
								}
							}
						});
                    }
                },
                remove: {
                    label: "Удалить",
                    action: function (obj) {
                        if (confirm("Вы уверены что хотите удалить объект?")) {
                            this.remove(obj);
                        }
                    }
                }
            }
        },
        html_data : {
            "data" : $("#tree").html(),
            "ajax" : {
                url : "tree/",
                type: "POST",
                data : function (node) { 
                    return { id : node.attr ? node.attr("id").replace('n','') : 0 };
				}
            }
        }
    })
    .bind("move_node.jstree", function (e, data) {
        var position={'last':'last-child','before':'left','after':'right'}[data.rslt.p];
        var target = data.rslt.np.attr("id").replace("n","");
        data.rslt.o.each(function (i) {
			$.ajax({
				async : false,
				type: 'POST',
				url: "move_node/",
				data : { 
					"node" : $(this).attr("id").replace("n",""), 
					"target" : data.rslt.r.attr("id").replace("n",""), 
					"position" : position
				},
                error: function(){
                    $.jstree.rollback(data.rlbk);
                }
			});
		});
	})
    .bind("rename.jstree", function (e, data) {
		$.ajax({
            async : false,
			url: "rename_node/", type: "POST",
			data: { 
				"node" : data.rslt.obj.attr("id").replace("n",""),
				"name" : data.rslt.new_name
			},
            error: function(){
                $.jstree.rollback(data.rlbk);
			},
            success: function(){
                data.rslt.obj.find('a:eq(0)').click();
			}
        });
	})
    .bind("create.jstree", function (e, data) {
		$.ajax({
            async : false,
			url: "add_node/",
            type: "POST",
			data: {
                'name': data.rslt.name,
                'parent': data.rslt.parent.attr("id").replace("n","")
            },
            dataType: "json",
            error: function(){
                $.jstree.rollback(data.rlbk);
                alert('Ошибка при добавлении страницы');
			},
            success: function(r){
                $(data.rslt.obj).attr("id", "n" + r.id);
                $(data.rslt.obj).find("a:eq(0)").attr("href", r.id+"/");
                $(data.rslt.obj).addClass("HiddenNode");
			}
        });
        return false;
	})
    .bind("remove.jstree", function (e, data) {
		data.rslt.obj.each(function () {
			$.ajax({
				async : false,
				type: 'POST',
				url: "remove_node/",
				data : {
					"node" : this.id.replace("n","")
				},
                error: function(){
                    $.jstree.rollback(data.rlbk);
                },
                success: function(){
                    $("#inline-formset").empty();
                }
			});
		});
	});
});