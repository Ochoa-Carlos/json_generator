import itertools
import calendar
from datetime import datetime, timedelta
from typing import Union, Optional, List, Dict, Any

from sqlalchemy.orm import Session
import traceback
from json_generator_disp.helpers.enumerators import ComplementTypeEnum
from json_generator_disp.helpers.constants import VERSION
from json_generator_disp.helpers.enumerators import CaracterEnum, SiNoEnum, ProductKeyEnum
from json_generator_disp.helpers.logger import logger
from json_generator_disp.models import MovimientoTanque as MovimientoTanqueModel
from json_generator_disp.models import MovimientoDispensario as MovimientoDispensarioModel
from json_generator_disp.models import Permiso
from json_generator_disp.models import Producto as ProductModel
from json_generator_disp.models import ExistenciaDTanque as ExistenciasDModel
from json_generator_disp.models import Cfdi as CfdiModel
from json_generator_disp.models import Manguera as MangueraModel
from json_generator_disp.models import Dictamen as DictamenModel
from json_generator_disp.models import Certificado as CertificadoModel
from json_generator_disp.models import Tanque as TanqueModel
from json_generator_disp.models import Dispensario as DispensarioModel
from json_generator_disp.models import MedidorDispensario
from json_generator_disp.services.volume_month_report import VolumeMonthlyReportJson
from json_generator_disp.services.complement_factory import ComplementFactory
from json_generator_disp.services.tank_movements import TankDeliveries, TankReceptions, Existances, Tank
from json_generator_disp.services.disp_movements import DispDeliveries, Dispensary
from json_generator_disp.services.repository import DbRepository
from json_generator_disp.utils.constants import DAILY_PRODUCT_DICT, MONTHLY_PRODUCT_DICT

logging = logger()

class ProductJson:
    """Root class for JSON."""

    def __init__(self, root: dict, date: Union[datetime, str], db_name: str):
        self.root = root
        self.date = date
        self.db_name = db_name

    def build_monthly_product(self, db: Session) -> dict:
        """Month product list"""
        print("BUILD PRODUCT")
        try:
            date_time = datetime.strptime(self.date, "%Y-%m-%d")
            date_now = datetime.now().strftime("%Y-%m-%d")
            year = date_time.year
            month = date_time.strftime('%m')
            first_day = date_time.strftime('%d')
            last_day = calendar.monthrange(year, date_time.month)[1]
            products_list = []

            products = db.query(ProductModel).all()
            movements = db.query(MovimientoTanqueModel).filter(
                MovimientoTanqueModel.fechaYHIM.between(
                    f'{year}-{month}-{first_day} 00:00:00',
                    f'{year}-{month}-{last_day} 23:59:59'
                )).all()
            existances = db.query(ExistenciasDModel).order_by(
                ExistenciasDModel.fechaYHEM).filter(ExistenciasDModel.fechaYHEM.between(
                    f'{year}-{month}-{first_day} 00:00:00',
                    f'{year}-{month}-{last_day} 23:59:59'
                )).all()
            cfdis = db.query(CfdiModel).order_by(
                CfdiModel.fechaYHT).filter(CfdiModel.fechaYHT.between(
                    f'{year}-{month}-{first_day} 00:00:00',
                    f'{year}-{month}-{last_day} 23:59:59'
                )).all()
            dictamen = db.query(DictamenModel).filter().first()
            certificate = db.query(CertificadoModel).filter().first()

            for product in products:
                prod_dict = {
                    "ClaveProducto": None,
                    "ClaveSubProducto": None,
                    "ReporteDeVolumenMensual": None,
                    "ComposOctanajeGasolina": None,
                    "GasolinaConCombustibleNoFosil": None,
                    "ComposDeCombustibleNoFosilEnGasolina": None,
                    "DieselConCombustibleNoFosil": None,
                    "ComposDeCombustibleNoFosilEnDiesel": None,
                    "TurbosinaConCombustibleNoFosil": None,
                    "ComposDeCombustibleNoFosilEnTurbosina": None,
                    "ComposDePropanoEnGasLP": None,
                    "ComposDeButanoEnGasLP": None,
                    "DensidadDePetroleo": None,
                    "ComposDeAzufreEnPetroleo": None,
                    "Otros": None,
                    "MarcaComercial": None,
                    "Marcaje": None,
                    "ConcentracionSustanciaMarcaje": None,
                    "GasNaturalOCondensados": None,
                }
                deliveries = [mov for mov in movements
                              if mov.movimiento == "Entrega" and mov.claveSubProducto == product.claveSubProducto]
                receptions = [mov for mov in movements
                              if mov.movimiento == "Recepcion" and mov.claveSubProducto == product.claveSubProducto]

                prod_dict.update({"ClaveProducto": product.claveProducto})
                prod_dict.update(self._build_product_key_data(product_dict=prod_dict, product=product))
                prod_dict.update(self._build_otros(product_dict=prod_dict, product=product))
                prod_dict.update(self._build_volume_month_report(
                    product=product,
                    existances=existances,
                    receptions=receptions,
                    deliveries=deliveries,
                    dictamen=dictamen,
                    certificate=certificate,
                    cfdis=cfdis
                    ))
                prod_dict.update(self._build_gasnatural_condensados(product=product))
                products_list.append(prod_dict) 

                for key in list(prod_dict.keys()):
                    if prod_dict[key] is None:
                        prod_dict.pop(key)

            self.root["Producto"].extend(products_list)
            return self.root

        except Exception as exc:
            trace = traceback.extract_tb(exc.__traceback__)[-1]
            logging.error(f"Error al construir producto {exc}")
            logging.error(f"Error en archivo {trace.filename}, línea {trace.lineno}, función {trace.name}")
            logging.error(traceback.format_exc().strip().split("\n")[-2])
            return {}

    def build_daily_product(self, db: Session) -> dict:
        """Daily product list"""
        print("BUILD DAILY PRODUCT")
        try:
            date_time = datetime.strptime(self.date, "%Y-%m-%d")
            date_now = datetime.now().strftime("%Y-%m-%d")
            year = date_time.year
            month = date_time.strftime('%m')
            first_day = date_time.strftime('%d')
            last_day = calendar.monthrange(year, date_time.month)[1]
            products_list = []

            data_repository = DbRepository(db=db)

            products = data_repository.get_products()
            receptions = data_repository.get_receptions(
                from_date=f'{year}-{month}-{first_day} 00:00:00',
                to_date=f'{year}-{month}-{first_day} 23:59:59'
                )
            deliveries = data_repository.get_deliveries(
                from_date=f'{year}-{month}-{first_day} 00:00:00',
                to_date=f'{year}-{month}-{first_day} 23:59:59'
            )
            day_existance = data_repository.get_day_existance(
                from_date=f'{year}-{month}-{first_day} 00:00:00',
                to_date=f'{year}-{month}-{first_day} 23:59:59'
            )
            cfdis = [item.cfdi_rel for item in itertools.chain(receptions, deliveries) if item.cfdi]

            dictamen = data_repository.get_dictamen()
            certificate = data_repository.get_certificate()
            tanks = data_repository.get_tanks()
            disps = data_repository.get_dispensarios()
            print("=====================", "JSON DIARIO")

            for product in products:
                # Dict for product to being build
                prod_dict = DAILY_PRODUCT_DICT.copy()

                tanks = data_repository.get_tanks_by_product(product_id=product.idProducto)
                tank_list = []
                disps = data_repository.get_dispensarios()
                disp_list = []
                medidores_disp = db.query(MedidorDispensario).all()
                medidores_disp = data_repository.get_disp_medidores()
                mangueras = db.query(MangueraModel).all()

                prod_dict.update({"ClaveProducto": product.claveProducto})
                prod_dict.update(self._build_product_key_data(product_dict=prod_dict, product=product))
                prod_dict.update(self._build_otros(product_dict=prod_dict, product=product))
                prod_dict.update(self._build_gasnatural_condensados(product=product))

                for tank in tanks:
                    tank_list.append(self._get_tanque(
                        tank=tank, movements=receptions, day_existance=day_existance)
                        )
                for disp in disps:
                    disp_list.append(self._get_dispensario(
                        disp=disp, movements=deliveries,
                        subprod_key=product.claveSubProducto,
                        medidores=medidores_disp, mangueras=mangueras)
                        )
                if tank_list:
                    prod_dict["Tanque"] = tank_list
                if disp_list:
                    prod_dict["Dispensario"] = disp_list

                products_list.append(prod_dict)
                for key in list(prod_dict.keys()):
                    if prod_dict[key] is None:
                        prod_dict.pop(key)

            self.root["Producto"].extend(products_list)

            return self.root

        except Exception as exc:
            trace = traceback.extract_tb(exc.__traceback__)[-1]
            logging.error(f"Error al construir producto {exc}")
            logging.error(f"Error en archivo {trace.filename}, línea {trace.lineno}, función {trace.name}")
            logging.error(traceback.format_exc().strip().split("\n")[-2])
            return {}

    def _build_product_key_data(self, product_dict: Dict[str, Any], product: ProductModel) -> Dict[str, Any]:
        """Build Dict with data according product key.
        :param product_dict: builded Dict of product if is needed.
        :param product: ddbb product obj.
        :return: Dictionary according type of product."""
        data = {}

        if product.claveProducto in ["PR03", "PR07", "PR08", "PR09", "PR11",
                                     "PR13", "PR15", "PR16", "PR17", "PR18", "PR19"]:
            data["ClaveSubProducto"] = product.claveSubProducto

        if product.claveProducto == "PR03":
            data["DieselConCombustibleNoFosil"] = product.dieselCCNF

            if data["DieselConCombustibleNoFosil"] == SiNoEnum.SI.value:
                data["ComposDeCombustibleNoFosilEnDiesel"] = product.composiciones.composDCNFED

        if product.claveProducto == "PR07":
            data["ComposOctanajeGasolina"] = product.composiciones.composOG
            data["GasolinaConCombustibleNoFosil"] = product.gasolinaCCNF

            if data["GasolinaConCombustibleNoFosil"] == SiNoEnum.SI.value:
                data["ComposDeCombustibleNoFosilEnGasolina"] = product.composiciones.composDCNFEG

        if product.claveProducto == "PR08":
            if self.root.get("Caracter") in ["contratista", "asignatario"]:
                data["DensidadDePetroleo"] = product.composiciones.densidadDePetroleo
                data["ComposDeAzufreEnPetroleo"] = product.composiciones.composDAEP

        if product.claveProducto == "PR11":
            data["TurbosinaConCombustibleNoFosil"] = product.turbosinaCCNF

            if data["TurbosinaConCombustibleNoFosil"] == SiNoEnum.SI.value:
                data["ComposDeCombustibleNoFosilEnTurbosina"] = product.composiciones.composDCNFET

        if product.claveProducto == "PR12":
            data["ComposDePropanoEnGasLP"] = product.composiciones.composDPEGLP
            data["ComposDeButanoEnGasLP"] = product.composiciones.composDBEGLP

        if product.claveProducto == "PR15":
            if product.claveSubProducto == "SP20":
                data["Otros"] = product.otros

        return data

    def _build_otros(self, product_dict: Dict[str, Any], product: ProductModel) -> Dict[str, Any]:
        """Build Dict with other's field data.
        :param product_dict: builded Dict of product if is needed.
        :param product: ddbb product obj.
        :return: Dictionary."""
        data = {}

        if product.marcaComercial:
            data["MarcaComercial"] = product.marcaComercial

        if product.marcaje:
            data["Marcaje"] = product.marcaje
            data["ConcentracionSustanciaMarcaje"] = product.concentracionSustanciaMarcaje

        return data

    def _build_volume_month_report(self,
                                   product: ProductModel,
                                   existances: Optional[ExistenciasDModel],
                                   receptions: MovimientoTanqueModel,
                                   deliveries: MovimientoTanqueModel,
                                   dictamen: Optional[DictamenModel],
                                   certificate: Optional[CertificadoModel],
                                   cfdis: CfdiModel)  -> dict:
        """Generate ReporteVolumenMensual key."""
        report_obj = VolumeMonthlyReportJson(
            receptions=receptions, deliveries=deliveries, dictamen=dictamen,
            certificate=certificate, product=product, existances=existances, cfdis=cfdis)
        month_report = report_obj.build_month_report(date=self.date)

        return {
            "ReporteDeVolumenMensual": month_report
        }

    def _build_gasnatural_condensados(self, product: ProductModel) -> Dict[str, Any]:
        """Build Dict of PR09 and PR10 specific data.
        :param product: ddbb product obj.
        :return: Dictionary with GasNaturalOCondensados data."""
        data = {}

        if product.claveProducto in ["PR09", "PR10"]:
            data["ComposGasNaturalOCondensados"] = product.gasNaturalOCondensados
            data["FraccionMolar"] = product.fraccionMolar
            data["PoderCalorifico"] = product.composiciones.poderCalorifico
            return {"GasNaturalOCondensados": data}

        return data

    # ================================= DAILY CODE =================================

    def _get_tanque(self,
                      tank: TanqueModel,
                      movements: List[MovimientoTanqueModel],
                      day_existance: ExistenciasDModel) -> Dict[str, Any]:
        """Build Dict with data of Tanque.
        :param tank: ddbb TanqueModel obj.
        :param movements: ddbb MovimientoTanqueModel obj.
        :return: Dictionary with movements data of the given tank."""
        movements = [mov for mov in movements if mov.claveIT == tank.claveIT]

        tank_obj = Tank(tank=tank, movements=movements, existances=day_existance)
        tank_data = tank_obj.build_tank_data()

        return tank_data

    def _get_dispensario(self, disp: DispensarioModel, movements: List[MovimientoDispensarioModel], subprod_key: int,
                    medidores: List[MedidorDispensario], mangueras: List[MangueraModel]) -> Dict[str, Dict]:
        # """Return a dict with the dispensary data in."""
        """:param subprod_key: claveSubProducto value.
        :param disp: ddbb DispensarioModel obj.
        :param movements: ddbb MovimientoDispensarioModel obj where movimiento attr == "Entrega".
        :param medidores: ddbb MedidorDispensarioModel list objs.
        :param mangueras: ddbb MangueraModel list objs."""
        movements = [deliv for deliv in movements if deliv.claveSubProducto == subprod_key]
        mangueras = [mang for mang in mangueras if mang.idDispensario == disp.idDispensario]
        mangueras_ids = {mang.idManguera for mang in mangueras if mang.idDispensario == disp.idDispensario}
        medidores = [med for med in medidores if med.idManguera in mangueras_ids]

        disp_obj = Dispensary(subprod_key=subprod_key, disp=disp, movements=movements, medidores=medidores,
                              mangueras=mangueras)
        disp_data = disp_obj.build_dispensary_data()

        return disp_data
