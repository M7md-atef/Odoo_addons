import { Component, t, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { badgeTagProps } from "@web/core/tags_list/badge_tag";
import {
    Many2ManyTagsField,
    many2ManyTagsField,
} from "@web/views/fields/many2many_tags/many2many_tags_field";

class LeadColorTag extends Component {
    static template = "core_crm.LeadColorTag";

    props = useProps({
        ...badgeTagProps,
        hexColor: t.string(),
    });
}

class LeadColorTagsField extends Many2ManyTagsField {
    static components = {
        ...Many2ManyTagsField.components,
        Tag: LeadColorTag,
    };

    getTagProps(record) {
        const props = super.getTagProps(record);
        delete props.color;
        return {
            ...props,
            hexColor: record.data.color || "#FC5130",
        };
    }
}

registry.category("fields").add("lead_color_tags", {
    ...many2ManyTagsField,
    component: LeadColorTagsField,
    relatedFields: () => [
        { name: "display_name", type: "char" },
        { name: "color", type: "char" },
    ],
});
