from sqlalchemy import Column, DateTime, ForeignKey, UUID, func


class ModelColumns:
    @staticmethod
    def created_at(nullable: bool = False):
        return Column(DateTime(timezone=True), nullable=nullable, server_default=func.now())

    @staticmethod
    def updated_at(nullable: bool = True):
        return Column(DateTime(timezone=True), nullable=nullable, onupdate=func.now())

    @staticmethod
    def deleted_at(nullable: bool = True):
        return Column(DateTime(timezone=True), nullable=nullable)

    @staticmethod
    def created_by_user(nullable: bool = True):
        return Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=nullable)

    @staticmethod
    def updated_by_user(nullable: bool = True):
        return Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=nullable)

    @staticmethod
    def deleted_by_user(nullable: bool = True):
        return Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=nullable)

    @staticmethod
    def created_by_project_member(nullable: bool = True):
        return Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=nullable)

    @staticmethod
    def updated_by_project_member(nullable: bool = True):
        return Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=nullable)

    @staticmethod
    def deleted_by_project_member(nullable: bool = True):
        return Column(UUID(as_uuid=True), ForeignKey("project_members.id"), nullable=nullable)
