// Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
// This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
// conditions defined in the file COPYING, which is part of this source code package.

//#   +--------------------------------------------------------------------+
//#   | Floating popup menus with content fetched via AJAX calls           |
//#   '--------------------------------------------------------------------'

import * as utils from "utils";
import * as ajax from "ajax";
import * as valuespecs from "valuespecs";

var active_popup = popup_context();

function popup_context() {
    const popup = {
        id: null,
        data: null,
        onclose: null
    };

    popup.popup = function() {
        return document.getElementById("popup_menu");
    };

    popup.container = function() {
        // FIXME: Ideally we could use getElementById directly to get the
        //        container. Unfortunately, many HTML elements used for
        //        popups do NOT have a unique ID. An example is the hamburger
        //        menu in the "All services" view where all menus share the
        //        same ID.
        //        This also causes the bug that two clicks are necessary to
        //        close the active popup and to open a popup of the same
        //        kind.
        //        To fix this issues all call sites of (render_)popup_trigger
        //        have to berefactored so that all IDs are unique.
        const popup = this.popup();
        return popup ? popup.parentNode : null;
    };

    popup.register = function(spec) {
        spec = spec || {};
        this.id = spec.id || null;
        this.data = spec.data || null;
        this.conclose = spec.onclose || null;

        if (this.id) {
            utils.add_event_handler("click", handle_popup_close);
        }
    };

    popup.close = function() {
        if (this.id) {
            utils.del_event_handler("click", handle_popup_close);
        }

        if (this.onclose) {
            eval(this.onclose);
        }

        this.id = null;
        this.data = null;
        this.onclose = null;
    };

    return popup;
}

export function close_popup()
{
    const menu = active_popup.popup();
    const container = active_popup.container();
    if (menu) {
        container.removeChild(menu);
    }

    active_popup.close();
}

// Registerd as click handler on the page while the popup menu is opened
// This is used to close the menu when the user clicks elsewhere
function handle_popup_close(event) {
    const container = active_popup.container();
    const target = utils.get_target(event);

    if (container.contains(target)) {
        return true; // clicked menu or statusicon
    }

    close_popup();
}

// event:       The browser event that triggered the action
// trigger_obj: DOM object of the action
// ident:       page global uinique identifier of the popup container
// method:      A JavaScript object that describes the method that is used
//              to add the content of the popup menu. The different methods
//              are distinguished by the attribute "type". Currently the
//              methods ajax, inline and colorpicker are supported.
//
//              ajax: Contains an attribute endpoint that used to construct the
//                    webservice url "ajax_popup_" + method.endpoint + ".py".
//                    The attribute url_vars contains the URL variables that are
//                    added to ajax_popup_*.py calls for rendering the popup menu.
//                    The url_vars may be null.
//
//              inline: The attribute content contains the string representation of
//                      the popup menu content.
//
//              colorpicker: Used to render color pickers. The object contains the
//                           attributes varprefix and value used to determine the
//                           ID of the color picker and its recent color.
//
// data:        JSON data which can be used by actions in popup menus
// onclose:     JavaScript code represented as a string that is evaluated when the
//              popup is closed
// resizable:   Allow the user to resize the popup by drag/drop (not persisted)
export function toggle_popup(event, trigger_obj, ident, method, data, onclose, resizable)
{
    if (!event)
        event = window.event;

    if (active_popup.id) {
        if (active_popup.id === ident) {
            close_popup();
            return; // same icon clicked: just close the menu
        } else {
            close_popup();
        }
    }

    active_popup.register({
        id: ident,
        data: data,
        onclose: onclose,
    });

    var container = trigger_obj.parentNode;

    let menu;
    if (method.type === "colorpicker") {
        menu = generate_colorpicker_body(trigger_obj, method.varprefix);
    } else {
        menu = document.createElement("div");
        menu.setAttribute("id", "popup_menu");
        menu.className = "popup_menu";

        var wrapper = document.createElement("div");
        wrapper.className = "wrapper";

        var content = document.createElement("div");
        content.className = "content";
        wrapper.appendChild(content);
        menu.appendChild(wrapper);
    }

    if (resizable)
        utils.add_class(menu, "resizable");

    container.appendChild(menu);
    fix_popup_menu_position(event, menu);

    if (method.type === "colorpicker") {
        /*The requirement for add_color_picker function to work is that the menu element is
        appended to the container element prior to the function call. In consequence, the
        add_color_picker function cannot not be called in the generate_colorpicker_body function.
        Modifying the add_color_picker to take elements as arguments will also not work in the
        current iteration due to the restrictions of the Colorpicker function. The Colorpicker
        prerequisites the current window as it accesses multiple attributes such as the
        offsetHeight of its slideElement
        */
        let rgb = trigger_obj.firstChild.style.backgroundColor;
        if (rgb !== "") {
            method.value = rgb2hex(rgb);
        }
        valuespecs.add_color_picker(method.varprefix, method.value);
    }

    if (resizable) {
        // Add a handle because we can not customize the styling of the default resize handle using css
        var resize = document.createElement("div");
        resize.className = "resizer";
        wrapper.appendChild(resize);
    }

    // update the menus contents using a webservice
    if (method.type === "ajax") {
        content.innerHTML = "<img src=\"themes/facelift/images/icon_reload.png\" class=\"icon reloading\">";
        const url_vars = !method.url_vars ? "" : "?" + method.url_vars;
        ajax.get_url("ajax_popup_" + method.endpoint + ".py" + url_vars, handle_render_popup_contents, {
            ident: ident,
            content: content,
            event: event,
        });
    } else if (method.type === "inline") {
        content.innerHTML = method.content;
        utils.execute_javascript_by_object(content);
    }
}

function generate_colorpicker_body(trigger_obj, varprefix)
{
    var menu = document.createElement("div");
    menu.setAttribute("id", "popup_menu");
    menu.className = "popup_menu";

    var wrapper = document.createElement("div");
    wrapper.className = "wrapper";
    menu.appendChild(wrapper);

    var content = document.createElement("div");
    content.className = "content";
    wrapper.appendChild(content);

    var picker = document.createElement("div");
    picker.className = "cp-small";
    picker.setAttribute("id", varprefix + "_picker");
    content.appendChild(picker)

    var cp_input = document.createElement("div");
    cp_input.className = "cp-input";
    cp_input.innerHTML = "Hex color:";
    content.appendChild(cp_input);

    var input_field = document.createElement("input");
    input_field.setAttribute("id", varprefix + "_input");
    input_field.setAttribute("type", "text");
    cp_input.appendChild(input_field);

    return menu;
}

function rgb2hex(rgb) {
    if (/^#[0-9A-F]{6}$/i.test(rgb)) return rgb;

    const matches = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);

    let hex_string = "#";
    for (let i = 1; i < matches.length; i++){
        hex_string += ("0" + parseInt(matches[i], 10).toString(16)).slice(-2);
    }
    return hex_string;
}


function handle_render_popup_contents(data, response_text)
{
    if (data.content) {
        data.content.innerHTML = response_text;
        fix_popup_menu_position(data.event, data.content);
    }
}

function fix_popup_menu_position(event, menu) {
    var rect = menu.getBoundingClientRect();

    // Check whether or not the menu is out of the bottom border
    // -> if so, move the menu up
    if (rect.bottom > (window.innerHeight || document.documentElement.clientHeight)) {
        var height = rect.bottom - rect.top;
        if (rect.top - height < 0) {
            // would hit the top border too, then put the menu to the top border
            // and hope that it fits within the screen
            menu.style.top    = "-" + (rect.top - 15) + "px";
            menu.style.bottom = "auto";
        } else {
            menu.style.top    = "auto";
            menu.style.bottom = "15px";
        }
    }

    // Check whether or not the menu is out of right border and
    // a move to the left would fix the issue
    // -> if so, move the menu to the left
    if (rect.right > (window.innerWidth || document.documentElement.clientWidth)) {
        var width = rect.right - rect.left;
        if (rect.left - width < 0) {
            // would hit the left border too, then put the menu to the left border
            // and hope that it fits within the screen
            menu.style.left  = "-" + (rect.left - 15) + "px";
            menu.style.right = "auto";
        } else {
            menu.style.left  = "auto";
            menu.style.right = "15px";
        }
    }
}

// TODO: Remove this function as soon as all visuals have been
// converted to pagetypes.py
export function add_to_visual(visual_type, visual_name)
{
    var element_type = active_popup.data[0];
    var create_info = {
        "context": active_popup.data[1],
        "params": active_popup.data[2],
    };
    var create_info_json = JSON.stringify(create_info);

    close_popup();

    var url = "ajax_add_visual.py"
        + "?visual_type=" + visual_type
        + "&visual_name=" + visual_name
        + "&type=" + element_type;

    ajax.call_ajax(url, {
        method : "POST",
        post_data: "create_info=" + encodeURIComponent(create_info_json),
        plain_error : true,
        response_handler: function(handler_data, response_body) {
            // After adding a dashlet, go to the choosen dashboard
            if (response_body.substr(0, 2) == "OK") {
                window.location.href = response_body.substr(3);
            } else {
                alert("Failed to add element: "+response_body);
            }
        }
    });
}

// FIXME: Adapt error handling which has been addded to add_to_visual() in the meantime
export function pagetype_add_to_container(page_type, page_name)
{
    var element_type = active_popup.data[0]; // e.g. "pnpgraph"
    // complex JSON struct describing the thing
    var create_info  = {
        "context"    : active_popup.data[1],
        "parameters" : active_popup.data[2]
    };
    var create_info_json = JSON.stringify(create_info);

    close_popup();

    var url = "ajax_pagetype_add_element.py"
              + "?page_type=" + page_type
              + "&page_name=" + page_name
              + "&element_type=" + element_type;

    ajax.call_ajax(url, {
        method           : "POST",
        post_data        : "create_info=" + encodeURIComponent(create_info_json),
        response_handler : function(handler_data, response_body) {
            // We get to lines of response. The first is an URL we should be
            // redirected to. The second is "true" if we should reload the
            // sidebar.
            if (response_body) {
                var parts = response_body.split("\n");
                if (parts[1] == "true")
                    utils.reload_sidebar();
                if (parts[0])
                    window.location.href = parts[0];
            }
        }
    });
}

export function graph_export(page)
{
    var request = {
        "specification": active_popup.data[2]["definition"]["specification"],
        "data_range": active_popup.data[2]["data_range"],
    };
    location.href = page + ".py?request=" + encodeURIComponent(JSON.stringify(request));
}
