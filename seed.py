from datetime import datetime, timedelta
from App.Core.Security.auth_user import handle_hash_password
from App.Database.database import SessionLocal
from App.Models.User import UserModel
from App.Models.Construction_sites import ConstructionModel
from App.Models.Site_member import SiteMemberModel
from App.Models.Work_items import WorkItemModel

db = SessionLocal()

try:
    user1 = UserModel(
        email="admin@gmail.com",
        password_hash=handle_hash_password('123'),
        full_name="Admin",
        role="Admin",
        is_active=True
    )

    user2 = UserModel(
        email="user1@gmail.com",
        password_hash=handle_hash_password('123'),
        full_name="Nguyen Van A",
        role="User",
        is_active=True
    )

    user3 = UserModel(
        email="user2@gmail.com",
        password_hash=handle_hash_password('123'),
        full_name="Nguyen Van B",
        role="User",
        is_active=True
    )
    db.add_all([user1, user2, user3])
    db.flush()
    construction1 = ConstructionModel(
        name="Công trình nhà phố Quận 7",
        description="Công trình nhà phố mẫu dùng để test API",
        owner_id=user2.id,
        create_at=datetime.now(),
        is_delete=False
    )

    construction2 = ConstructionModel(
        name="Công trình văn phòng",
        description="Công trình văn phòng mẫu phục vụ demo",
        owner_id=user3.id,
        create_at=datetime.now(),
        is_delete=False
    )

    db.add_all([construction1, construction2])
    db.flush()


    # =========================
    # 3. THÊM THÀNH VIÊN
    # =========================

    member1 = SiteMemberModel(
        site_id=construction1.id,
        user_id=user2.id,
        role="Owner",
        joined_at=datetime.now()
    )

    member2 = SiteMemberModel(
        site_id=construction1.id,
        user_id=user3.id,
        role="Member",
        joined_at=datetime.now()
    )

    member3 = SiteMemberModel(
        site_id=construction2.id,
        user_id=user3.id,
        role="Owner",
        joined_at=datetime.now()
    )

    member4 = SiteMemberModel(
        site_id=construction2.id,
        user_id=user2.id,
        role="Member",
        joined_at=datetime.now()
    )

    db.add_all([
        member1,
        member2,
        member3,
        member4
    ])


    # =========================
    # 4. TẠO WORK ITEM
    # =========================

    work1 = WorkItemModel(
        site_id=construction1.id,
        title="Đổ móng",
        description="Thi công phần móng công trình",
        assignee_id=user2.id,
        status="Pending",
        priority="High",
        due_date=datetime.now() + timedelta(days=3)
    )

    work2 = WorkItemModel(
        site_id=construction1.id,
        title="Xây tường",
        description="Xây tường tầng 1",
        assignee_id=user3.id,
        status="In Progress",
        priority="Medium",
        due_date=datetime.now() + timedelta(days=7)
    )

    work3 = WorkItemModel(
        site_id=construction1.id,
        title="Lắp đặt điện",
        description="Lắp đặt hệ thống điện",
        assignee_id=user3.id,
        status="Pending",
        priority="Low",
        due_date=datetime.now() + timedelta(days=14)
    )

    work4 = WorkItemModel(
        site_id=construction2.id,
        title="Thi công sàn",
        description="Thi công sàn tầng 1",
        assignee_id=user3.id,
        status="In Progress",
        priority="High",
        due_date=datetime.now() + timedelta(days=5)
    )

    work5 = WorkItemModel(
        site_id=construction2.id,
        title="Lắp cửa",
        description="Lắp đặt cửa ra vào",
        assignee_id=user2.id,
        status="Pending",
        priority="Medium",
        due_date=datetime.now() + timedelta(days=10)
    )

    work6 = WorkItemModel(
        site_id=construction2.id,
        title="Sơn tường",
        description="Sơn hoàn thiện tường",
        assignee_id=user2.id,
        status="Completed",
        priority="Low",
        due_date=datetime.now() + timedelta(days=2)
    )

    db.add_all([
        work1,
        work2,
        work3,
        work4,
        work5,
        work6
    ])
    db.commit()
    print("===================================")
    print("Seed dữ liệu thành công!")
    print("===================================")
    print("Users: 3")
    print("Construction: 2")
    print("Site members: 4")
    print("Work items: 6")
    print("===================================")
except Exception as e:
    db.rollback()
    print("Seed dữ liệu thất bại!")
    print("Error:", e)
finally:
    db.close()