from app import db
from API.Wacs import GetAllAssetsBase
from tables import Asset, Asset_brands, Asset_model, Asset_status, Asset_type


def SyncDBassets_Wacs():

    wacs_assets_base = GetAllAssetsBase()
    for wacs_asset in wacs_assets_base:
        wacs_id = wacs_asset['AssetID']
        name = wacs_asset['Name']
        vin = wacs_asset['Code']
        licenseplate = wacs_asset['Header1']
        milles = wacs_asset['MileageField']
        as_brand = Asset_brands.query.filter_by(name=wacs_asset['Brand']).first()
        if as_brand == None:
            as_brand = Asset_brands(name=wacs_asset['Brand'])
            db.session.add(as_brand)
            db.session.commit()
        model = Asset_model.query.filter_by(name=wacs_asset['Header3']).first()
        if model == None:
            model = Asset_model(name=wacs_asset['Header3'])
            db.session.add(model)
            db.session.commit()
        type = Asset_type.query.filter_by(name=wacs_asset['Type']).first()
        if type == None:
            type = Asset_type(name=wacs_asset['Type'])
            db.session.add(model)
            db.session.commit()
        if wacs_asset['Active']:
            stat = Asset_status.query.filter_by(name='active').first()
        else:
            stat = Asset_status.query.filter_by(name='inactive').first()

        app_asset = Asset.query.filter_by(wacs_id=wacs_asset['AssetID']).first()
        app_vin = Asset.query.filter_by(wacs_id=licenseplate).first()
        app_name = Asset.query.filter_by(wacs_id=name).first()

        if app_asset == None and app_vin and app_name and wacs_asset['Active']:
            new_asset = Asset(name=name,
                              vin=vin,
                              licenseplate=licenseplate,
                              wacs_id=wacs_id,
                              milles=milles
                              )
            as_brand.asset_id.append(new_asset)
            model.asset_id.append(new_asset)
            stat.asset_id.append(new_asset)
            new_asset.status = stat
            db.session.add(new_asset)
            db.session.commit()
        elif app_asset != None:
            app_asset.name = name
            app_asset.vin = vin
            app_asset.licenseplate = licenseplate
            app_asset.milles = milles
            db.session.commit()











SyncDBassets_Wacs()