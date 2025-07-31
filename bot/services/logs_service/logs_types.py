from typing import TypedDict
from abc import abstractmethod
from enum import StrEnum, auto
from disnake import Embed, Member, Role

from ...core.models import ReportModel
from ...core.base_embeds import InfoEmbed


class LogsTypesEnum(StrEnum):
    REPORT_SENDED = "REPORT_SENDED"
    REPORT_CLOSED = "REPORT_CLOSED"
    MEMBER_ADDED_TO_REPORT_TICKET = "MEMBER_ADDED_TO_REPORT_TICKET"
    MEMBER_REMOVED_FROM_REPORT_TICKET = "MEMBER_REMOVED_FROM_REPORT_TICKET"
    REPORTS_ADMIN_ROLE_ADDED = "REPORTS_ADMIN_ROLE_ADDED"
    REPORTS_ADMIN_ROLE_REMOVED = "REPORTS_ADMIN_ROLE_REMOVED"


class BaseLogsType:
    def __init__(self, name: LogsTypesEnum):
        self.name = name

    @abstractmethod
    def get_message_embed(self) -> Embed: ...


class ReportsAdminRoleAdded(BaseLogsType):
    def __init__(self, role: Role):
        super().__init__(name=LogsTypesEnum.REPORT_SENDED)
        self.role = role

    def get_message_embed(self) -> Embed:
        return InfoEmbed(description=f"Reports admin role was added").add_field(
            "Role",
            self.role.mention,
        )


class ReportsAdminRoleRemoved(BaseLogsType):
    def __init__(self, role: Role):
        super().__init__(name=LogsTypesEnum.REPORT_SENDED)
        self.role = role

    def get_message_embed(self) -> Embed:
        return InfoEmbed(description=f"Reports admin role was removed").add_field(
            "Role",
            self.role.mention,
        )


class ReportClosed(BaseLogsType):
    def __init__(self, report: ReportModel):
        super().__init__(name=LogsTypesEnum.REPORT_CLOSED)
        self.report = report

    def get_message_embed(self) -> Embed:
        return (
            InfoEmbed(description=f"Report has closed")
            .add_field(
                "Channel id",
                f"<#{self.report.channel_id}>",
            )
            .add_field(
                "Result",
                self.report.result_text,
            )
            .add_field(
                "Report ID",
                self.report.id,
            )
        )


class MemberAddedToReportChannel(BaseLogsType):
    def __init__(
        self,
        report: ReportModel,
        member: Member,
    ):
        super().__init__(name=LogsTypesEnum.MEMBER_ADDED_TO_REPORT_TICKET)
        self.report = report
        self.member = member

    def get_message_embed(self) -> Embed:
        return (
            InfoEmbed(description=f"Member has added to report channel.")
            .add_field(
                "Channel id",
                f"<#{self.report.channel_id}>",
            )
            .add_field(
                "Member",
                self.member.mention,
            )
            .add_field(
                "Report ID",
                self.report.id,
            )
        )


class MemberRemovedFromReportChannel(BaseLogsType):
    def __init__(
        self,
        report: ReportModel,
        member: Member,
    ):
        super().__init__(name=LogsTypesEnum.MEMBER_REMOVED_FROM_REPORT_TICKET)
        self.report = report
        self.member = member

    def get_message_embed(self) -> Embed:
        return (
            InfoEmbed(description=f"Member has removed from report channel.")
            .add_field(
                "Channel id",
                f"<#{self.report.channel_id}>",
            )
            .add_field(
                "Member",
                self.member.mention,
            )
            .add_field(
                "Report ID",
                self.report.id,
            )
        )
