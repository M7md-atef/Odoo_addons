import { Component, proxy, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";
import { useX2ManyCrud } from "@web/views/fields/relational_utils";

export class LeadTagList extends Component {
    static template = "core_crm.LeadTagList";

    props = useProps({
        ...standardFieldProps,
    });

    setup() {
        this.orm = useService("orm");
        this.state = proxy({ open: false, available: [] });
        const { saveRecord } = useX2ManyCrud(
            () => this.props.record.data[this.props.name],
            true
        );
        this.saveRecord = saveRecord;
        this.loadTags();
    }

    async loadTags() {
        this.state.available = await this.orm.searchRead(
            "core.crm.tag",
            [],
            ["name", "color"],
            { order: "name" }
        );
    }

    get tags() {
        const field = this.props.record.data[this.props.name];
        return field ? field.records || [] : [];
    }

    isSelected(tag) {
        return this.tags.some((selected) => selected.resId === tag.id);
    }

    toggleMenu() {
        if (!this.props.readonly) {
            this.state.open = !this.state.open;
        }
    }

    async toggleTag(tag) {
        const selected = this.tags.find((item) => item.resId === tag.id);
        if (selected) {
            await this.props.record.data[this.props.name].forget(selected);
        } else {
            await this.saveRecord([tag.id]);
        }
    }
}

registry.category("fields").add("lead_tag_list", {
    component: LeadTagList,
    supportedTypes: ["many2many"],
    relatedFields: () => [
        { name: "name", type: "char" },
        { name: "color", type: "char" },
    ],
});
