# Generated by Django 3.2.8 on 2021-12-04 16:58

from django.db import migrations


def initial_data(apps, schema_editor):
    unit_model = apps.get_model("api_beer", "BeerUnit")
    nation_model = apps.get_model("api_beer", "Nation")
    producer_model = apps.get_model("api_beer", "Producer")
    beer_model = apps.get_model("api_beer", "Beer")

    units = [
        unit_model(name="Lon"),
        unit_model(name="Hộp"),
        unit_model(name="Chai")
    ]
    unit_model.objects.bulk_create(units)

    loc_unit = unit_model(name="Lốc")
    thung_unit = unit_model(name="Thùng")
    loc_unit.save()
    thung_unit.save()

    nations = [
        nation_model(name="Mexico",
                     flag_picture='https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638121/SGroup/KOB/nations/mexico_jnwrnn.png'),
        nation_model(name="Singapore",
                     flag_picture='https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638083/SGroup/KOB/nations/singapore_va8ebk.png'),
        nation_model(name="France",
                     flag_picture='https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638055/SGroup/KOB/nations/france_k2kht3.png'),
        nation_model(name="USA",
                     flag_picture='https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638034/SGroup/KOB/nations/united-states_imyw4u.png')
    ]
    nation_model.objects.bulk_create(nations)

    vietnam = nation_model(name="Việt Nam",
                 flag_picture='https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638012/SGroup/KOB/nations/vietnam_1_wftv2l.png')
    netherlands = nation_model(name="Hà Lan",
                           flag_picture='https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638899/SGroup/KOB/nations/netherlands_aafwe0.png')
    vietnam.save()
    netherlands.save()

    producer_heineken = producer_model.objects.filter(name='Nhà máy Bia Heineken Đà Nẵng').first()

    beers = [
        beer_model(name="Heineken Silver",
                   alcohol_concentration=4,
                   capacity='330ml',
                   origin_nation=vietnam,
                   price=450000,
                   bottle_amount=24,
                   describe='Bia là một loại thức uống có còn chiều lòng được nhiều cánh đàn ông và cả chị em phụ nữ. Năm trước bia Heineken Silver đã được ra mắt và nhanh chóng tạo cơ sốt và rất được yêu thích. Thậm chí loại bia này đã được đặt lên bàn cân với nhiều loại bia khác',
                   producer=producer_heineken,
                   beer_unit=thung_unit),
        beer_model(name="Heineken Sleek",
                   alcohol_concentration=5,
                   capacity='330ml',
                   origin_nation=netherlands,
                   price=115000,
                   bottle_amount=6,
                   describe='Ưu tiên hàng đầu của Heineken luôn rõ ràng: chất lượng tuyệt hảo đặt lên trên hiệu quả kinh tế.Hướng dẫn sử dụng: dùng trực tiếp, ướp lạnh, hoặc dùng với đá. Ngon hơn khi uống lạnh.Hướng dẫn bảo quản:- Bảo quản nơi sạch sẽ, khô ráo thoáng mát.- Tránh ánh nắng mặt trời',
                   producer=producer_heineken,
                   beer_unit=loc_unit),
    ]
    beer_model.objects.bulk_create(beers)


class Migration(migrations.Migration):

    dependencies = [
        ('api_beer', '0003_beer_beerunit_nation'),
    ]

    operations = [
        migrations.RunPython(initial_data, migrations.RunPython.noop)
    ]
