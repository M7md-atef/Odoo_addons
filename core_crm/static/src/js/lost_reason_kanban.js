import { onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";

class LostReasonKanbanRenderer extends KanbanRenderer {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
        this.lostStageIds = new Set();
        onWillStart(async () => {
            const stages = await this.orm.searchRead(
                "core.crm.stage",
                [["is_lost", "=", true]],
                ["id"]
            );
            this.lostStageIds = new Set(stages.map((stage) => stage.id));
        });
    }

    async sortRecordDrop(dataRecordId, params) {
        const targetGroup = this.props.list.groups.find(
            (group) => group.id === params.parent?.dataset.id
        );
        if (!targetGroup || !this.lostStageIds.has(targetGroup.value)) {
            return super.sortRecordDrop(dataRecordId, params);
        }

        const draggedIds = this.multiDragRecordIds || [dataRecordId];
        const leadIds = this.props.list.records
            .filter(
                (record) =>
                    draggedIds.includes(record.id) &&
                    !this.lostStageIds.has(record.group.value)
            )
            .map((record) => record.resId);
        if (!leadIds.length) {
            return super.sortRecordDrop(dataRecordId, params);
        }

        return this.action.doAction("core_crm.action_core_crm_lead_lost_wizard", {
            additionalContext: {
                active_ids: leadIds,
                default_lead_ids: [[6, 0, leadIds]],
                default_stage_id: targetGroup.value,
            },
            onClose: () => this.props.list.model.load(),
        });
    }
}

registry.category("views").add("core_crm_lost_reason_kanban", {
    ...kanbanView,
    Renderer: LostReasonKanbanRenderer,
});
