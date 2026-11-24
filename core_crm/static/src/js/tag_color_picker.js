import { Component, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class TagColorPicker extends Component {
    static template = "core_crm.TagColorPicker";

    props = useProps({
        ...standardFieldProps,
    });

    get color() {
        return this.props.record.data[this.props.name] || "#FC5130";
    }

    onColorChange(event) {
        this.props.record.update({
            [this.props.name]: event.target.value.toUpperCase(),
        });
    }

    onHexInput(event) {
        let value = event.target.value.trim();
        if (value && value[0] !== "#") {
            value = `#${value}`;
        }
        if (/^#[0-9A-Fa-f]{6}$/.test(value)) {
            this.props.record.update({
                [this.props.name]: value.toUpperCase(),
            });
        }
    }
}

registry.category("fields").add("tag_color_picker", {
    component: TagColorPicker,
    supportedTypes: ["char"],
});
