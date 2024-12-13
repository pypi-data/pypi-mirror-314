import json_duplicate_keys as jdks

class intQR:
	def __init__(self, QR_Type, ordered_dict=False):
		self.QR_Type = QR_Type
		self.QR = jdks.loads("{}", ordered_dict=ordered_dict)

		self.QR.set("00", { "name":"PayloadFormatIndicator", "length":2, "value":"" })
		self.QR.set("01", { "name":"PointOfInitiationMethod", "length":2, "value":"" })


		if self.QR_Type in ["VietQR", "MoMo"]:
			self.QR.set("38", { "name":"MerchantAccountInformation", "length":99, "value":"", "subTag":{} })
			self.QR.set("38||subTag||00", { "name":"GUID", "length":32, "value":"" })
			self.QR.set("38||subTag||01", { "name":"BeneficiaryOrganization", "length":0, "value":"", "subTag":{} })
			self.QR.set("38||subTag||01||subTag||00", { "name":"BeneficiaryID", "length":6, "value":"" })
			self.QR.set("38||subTag||01||subTag||01", { "name":"ReceiverNumber", "length":19, "value":"" })
			self.QR.set("38||subTag||02", { "name":"ServiceCode", "length":10, "value":"" })

		elif self.QR_Type == "KHQR_Individual":
			self.QR.set("29", { "name":"MerchantAccountInformation", "length":99, "value":"", "subTag":{} })
			self.QR.set("29||subTag||00", { "name":"BakongAccountID", "length":32, "value":"" })
			self.QR.set("29||subTag||01", { "name":"AccountInformation", "length":32, "value":"" })
			self.QR.set("29||subTag||02", { "name":"AcquiringBank", "length":32, "value":"" })

		elif self.QR_Type == "KHQR_Corporate":
			self.QR.set("30", { "name":"MerchantAccountInformation", "length":99, "value":"", "subTag":{} })
			self.QR.set("30||subTag||00", { "name":"BakongAccountID", "length":32, "value":"" })
			self.QR.set("30||subTag||01", { "name":"MerchantID", "length":32, "value":"" })
			self.QR.set("30||subTag||02", { "name":"AcquiringBank", "length":32, "value":"" })


		self.QR.set("52", { "name":"MerchantCategoryCode", "length":4, "value":"" })
		self.QR.set("53", { "name":"TransactionCurrency", "length":3, "value":"" })
		self.QR.set("54", { "name":"TransactionAmount", "length":13, "value":"" })
		self.QR.set("55", { "name":"TipOrConvenienceIndicator", "length":2, "value":"" })
		self.QR.set("56", { "name":"ValueOfConvenienceFeeFixed", "length":13, "value":"" })
		self.QR.set("57", { "name":"ValueOfConvenienceFeePercentage", "length":5, "value":"" })
		self.QR.set("58", { "name":"CountryCode", "length":13, "value":"" })
		self.QR.set("59", { "name":"MerchantName", "length":25, "value":"" })
		self.QR.set("60", { "name":"MerchantCity", "length":15, "value":"" })
		self.QR.set("61", { "name":"PostalCode", "length":10, "value":"" })
		self.QR.set("62", { "name":"AdditionalDataFieldTemplate", "length":99, "value":"", "subTag":{} })
		self.QR.set("62||subTag||01", { "name":"BillNumber", "length":25, "value":"" })
		self.QR.set("62||subTag||02", { "name":"MobileNumber", "length":25, "value":"" })
		self.QR.set("62||subTag||03", { "name":"StoreLabel", "length":25, "value":"" })
		self.QR.set("62||subTag||04", { "name":"LoyaltyNumber", "length":25, "value":"" })
		self.QR.set("62||subTag||05", { "name":"ReferenceLabel", "length":25, "value":"" })
		self.QR.set("62||subTag||06", { "name":"CustomerLabel", "length":25, "value":"" })
		self.QR.set("62||subTag||07", { "name":"TerminalLabel", "length":25, "value":"" })
		self.QR.set("62||subTag||08", { "name":"PurposeOfTransaction", "length":25, "value":"" })
		self.QR.set("62||subTag||09", { "name":"AdditionalConsumerDataRequest", "length":3, "value":"" })
		self.QR.set("63", { "name":"CRC", "length":4, "value":"" })
		self.QR.set("64", { "name":"MerchantInformation_LanguageTemplate", "length":99, "value":"", "subTag":{} })
		self.QR.set("64||subTag||00", { "name":"LanguagePreference", "length":2, "value":"" })
		self.QR.set("64||subTag||01", { "name":"MerchantName_AlternateLanguage", "length":25, "value":"" })
		self.QR.set("64||subTag||02", { "name":"MerchantCity_AlternateLanguage", "length":15, "value":"" })

		if self.QR_Type == "MoMo":
			self.QR.set("80", { "name":"LastThreeDigitsOfPhoneNumber", "length":3, "value":"" })

		if self.QR_Type in ["KHQR_Individual", "KHQR_Corporate"]:
			self.QR.set("99", { "name":"Timestamp", "length":17, "value":"", "subTag":{} })
			self.QR.set("99||subTag||00", { "name":"timestamp", "length":13, "value":"" })



	def parse(self, QR_String, currentKey="", strict=True, ordered_dict=False):
		while len(QR_String) > 0:
			try:
				TAG = LENGTH = VALUE = ""
				TAG = QR_String[:2]; QR_String = QR_String[2:]
				LENGTH_STR = QR_String[:2]; QR_String = QR_String[2:]
				LENGTH = int(LENGTH_STR)
				VALUE = QR_String[:LENGTH]; QR_String = QR_String[LENGTH:]

				if self.QR.get(currentKey+TAG)["value"] == "JSON_DUPLICATE_KEYS_ERROR":
					self.QR.set(currentKey+TAG, { "name":"UnknownField", "length":LENGTH, "value":TAG+LENGTH_STR+VALUE })
				else:
					if strict:
						if (LENGTH <= self.QR.get(currentKey+TAG+"||length")["value"] or self.QR.get(currentKey+TAG+"||length")["value"] == 0) and LENGTH == len(VALUE):
							self.QR.update(currentKey+TAG+"||value", VALUE)
							if self.QR.get(currentKey+TAG+"||subTag")["value"] != "JSON_DUPLICATE_KEYS_ERROR":
								self.parse(VALUE, currentKey=self.QR.get(currentKey+TAG+"||subTag")["name"]+"||", strict=strict, ordered_dict=ordered_dict)
						else:
							print("- currentKey: {}".format(currentKey))
							print("- TAG: {}".format(TAG))
							print("- LENGTH: {}".format(LENGTH_STR))
							print("- VALUE: {}".format(VALUE))
							return
					else:
						if LENGTH == len(VALUE):
							self.QR.update(currentKey+TAG+"||value", VALUE)
							if self.QR.get(currentKey+TAG+"||subTag")["value"] != "JSON_DUPLICATE_KEYS_ERROR":
								self.parse(VALUE, currentKey=self.QR.get(currentKey+TAG+"||subTag")["name"]+"||", strict=strict, ordered_dict=ordered_dict)
						else:
							print("- currentKey: {}".format(currentKey))
							print("- TAG: {}".format(TAG))
							print("- LENGTH: {}".format(LENGTH_STR))
							print("- VALUE: {}".format(VALUE))
							return
			except Exception as e:
				print("- currentKey: {}".format(currentKey))
				print("- TAG: {}".format(TAG))
				print("- LENGTH: {}".format(LENGTH_STR))
				print("- VALUE: {}".format(VALUE))
				return

		if currentKey == "":
			QRObj = jdks.loads("{}", ordered_dict=ordered_dict)

			QR_byKeys = self.QR.filter_keys("\\|\\|name$")
			QR_byKeys.flatten()
			for k in QR_byKeys.getObject():
				kName = []
				QRObj_kName = []
				tags = k.split("||name",1)[0].split("||subTag||")
				for i in range(len(tags)):
					kName.append(tags[i])
					name = self.QR.get("||subTag||".join(kName)+"||name")["value"]
					value = self.QR.get("||subTag||".join(kName)+"||value")["value"]
					QRObj_kName.append(name)

					if len(value) > 0:
						if len(tags) == 1 or i == len(tags)-1:
							QRObj.update("||".join(QRObj_kName), value, allow_new_key=True)
						elif type(QRObj.get("||".join(QRObj_kName))["value"]) != dict:
							QRObj.update("||".join(QRObj_kName), {}, allow_new_key=True)
			return QRObj



	def unparse(self, QRObj, update_CRC=True):
		def calculate_crc16_ccitt_false(data):
			crc = 0xFFFF
			polynomial = 0x1021
			for byte in data:
				crc ^= (ord(byte) << 8)
				for _ in range(8):
					if crc & 0x8000:
						crc = (crc << 1) ^ polynomial
					else:
						crc <<= 1
				crc &= 0xFFFF
			return "{:04X}".format(crc)

		QR_String = ""

		TAG_00 = QRObj.get("PayloadFormatIndicator")
		if TAG_00["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_00["value"]) > 0: QR_String += "{}{:02}{}".format("00", len(TAG_00["value"]), TAG_00["value"])

		TAG_01 = QRObj.get("PointOfInitiationMethod")
		if TAG_01["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_01["value"]) > 0: QR_String += "{}{:02}{}".format("01", len(TAG_01["value"]), TAG_01["value"])

		if self.QR_Type in ["VietQR", "MoMo"]:
			TAG_38 = QRObj.get("MerchantAccountInformation")
			if TAG_38["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_38["value"]) > 0:
				TAG_38_val = ""
				TAG_3800 = QRObj.get("MerchantAccountInformation||GUID")
				if TAG_3800["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_3800["value"]) > 0: TAG_38_val += "{}{:02}{}".format("00", len(TAG_3800["value"]), TAG_3800["value"])

				TAG_3801 = QRObj.get("MerchantAccountInformation||BeneficiaryOrganization")
				if TAG_3801["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_3801["value"]) > 0:
					TAG_3801_val = ""
					TAG_380100 = QRObj.get("MerchantAccountInformation||BeneficiaryOrganization||BeneficiaryID")
					if TAG_380100["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_380100["value"]) > 0: TAG_3801_val += "{}{:02}{}".format("00", len(TAG_380100["value"]), TAG_380100["value"])

					TAG_380101 = QRObj.get("MerchantAccountInformation||BeneficiaryOrganization||ReceiverNumber")
					if TAG_380101["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_380101["value"]) > 0: TAG_3801_val += "{}{:02}{}".format("01", len(TAG_380101["value"]), TAG_380101["value"])

					TAG_38_val += "{}{:02}{}".format("01", len(TAG_3801_val), TAG_3801_val)

				TAG_3802 = QRObj.get("MerchantAccountInformation||ServiceCode")
				if TAG_3802["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_3802["value"]) > 0: TAG_38_val += "{}{:02}{}".format("02", len(TAG_3802["value"]), TAG_3802["value"])

				QR_String += "{}{:02}{}".format("38", len(TAG_38_val), TAG_38_val)
		elif self.QR_Type == "KHQR_Individual":
			TAG_29 = QRObj.get("MerchantAccountInformation")
			if TAG_29["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_29["value"]) > 0:
				TAG_29_val = ""
				TAG_2900 = QRObj.get("MerchantAccountInformation||BakongAccountID")
				if TAG_2900["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_2900["value"]) > 0: TAG_29_val += "{}{:02}{}".format("00", len(TAG_2900["value"]), TAG_2900["value"])

				TAG_2901 = QRObj.get("MerchantAccountInformation||AccountInformation")
				if TAG_2901["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_2901["value"]) > 0: TAG_29_val += "{}{:02}{}".format("01", len(TAG_2901["value"]), TAG_2901["value"])

				TAG_2902 = QRObj.get("MerchantAccountInformation||AcquiringBank")
				if TAG_2902["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_2902["value"]) > 0: TAG_29_val += "{}{:02}{}".format("02", len(TAG_2902["value"]), TAG_2902["value"])

				QR_String += "{}{:02}{}".format("29", len(TAG_29_val), TAG_29_val)
		elif self.QR_Type == "KHQR_Corporate":
			TAG_30 = QRObj.get("MerchantAccountInformation")
			if TAG_30["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_30["value"]) > 0:
				TAG_30_val = ""
				TAG_3000 = QRObj.get("MerchantAccountInformation||BakongAccountID")
				if TAG_3000["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_3000["value"]) > 0: TAG_30_val += "{}{:02}{}".format("00", len(TAG_3000["value"]), TAG_3000["value"])

				TAG_3001 = QRObj.get("MerchantAccountInformation||MerchantID")
				if TAG_3001["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_3001["value"]) > 0: TAG_30_val += "{}{:02}{}".format("01", len(TAG_3001["value"]), TAG_3001["value"])

				TAG_3002 = QRObj.get("MerchantAccountInformation||AcquiringBank")
				if TAG_3002["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_3002["value"]) > 0: TAG_30_val += "{}{:02}{}".format("02", len(TAG_3002["value"]), TAG_3002["value"])

				QR_String += "{}{:02}{}".format("30", len(TAG_30_val), TAG_30_val)

		TAG_52 = QRObj.get("MerchantCategoryCode")
		if TAG_52["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_52["value"]) > 0: QR_String += "{}{:02}{}".format("52", len(TAG_52["value"]), TAG_52["value"])

		TAG_53 = QRObj.get("TransactionCurrency")
		if TAG_53["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_53["value"]) > 0: QR_String += "{}{:02}{}".format("53", len(TAG_53["value"]), TAG_53["value"])

		TAG_54 = QRObj.get("TransactionAmount")
		if TAG_54["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_54["value"]) > 0: QR_String += "{}{:02}{}".format("54", len(TAG_54["value"]), TAG_54["value"])

		TAG_55 = QRObj.get("TipOrConvenienceIndicator")
		if TAG_55["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_55["value"]) > 0: QR_String += "{}{:02}{}".format("55", len(TAG_55["value"]), TAG_55["value"])

		TAG_56 = QRObj.get("ValueOfConvenienceFeeFixed")
		if TAG_56["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_56["value"]) > 0: QR_String += "{}{:02}{}".format("56", len(TAG_56["value"]), TAG_56["value"])

		TAG_57 = QRObj.get("ValueOfConvenienceFeePercentage")
		if TAG_57["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_57["value"]) > 0: QR_String += "{}{:02}{}".format("57", len(TAG_57["value"]), TAG_57["value"])

		TAG_58 = QRObj.get("CountryCode")
		if TAG_58["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_58["value"]) > 0: QR_String += "{}{:02}{}".format("58", len(TAG_58["value"]), TAG_58["value"])

		TAG_59 = QRObj.get("MerchantName")
		if TAG_59["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_59["value"]) > 0: QR_String += "{}{:02}{}".format("59", len(TAG_59["value"]), TAG_59["value"])

		TAG_60 = QRObj.get("MerchantCity")
		if TAG_60["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_60["value"]) > 0: QR_String += "{}{:02}{}".format("60", len(TAG_60["value"]), TAG_60["value"])

		TAG_61 = QRObj.get("PostalCode")
		if TAG_61["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_61["value"]) > 0: QR_String += "{}{:02}{}".format("61", len(TAG_61["value"]), TAG_61["value"])

		TAG_62 = QRObj.get("AdditionalDataFieldTemplate")
		if TAG_62["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_62["value"]) > 0:
			TAG_62_val = ""
			TAG_6201 = QRObj.get("AdditionalDataFieldTemplate||BillNumber")
			if TAG_6201["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6201["value"]) > 0: TAG_62_val += "{}{:02}{}".format("01", len(TAG_6201["value"]), TAG_6201["value"])

			TAG_6202 = QRObj.get("AdditionalDataFieldTemplate||MobileNumber")
			if TAG_6202["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6202["value"]) > 0: TAG_62_val += "{}{:02}{}".format("02", len(TAG_6202["value"]), TAG_6202["value"])

			TAG_6203 = QRObj.get("AdditionalDataFieldTemplate||StoreLabel")
			if TAG_6203["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6203["value"]) > 0: TAG_62_val += "{}{:02}{}".format("03", len(TAG_6203["value"]), TAG_6203["value"])

			TAG_6204 = QRObj.get("AdditionalDataFieldTemplate||LoyaltyNumber")
			if TAG_6204["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6204["value"]) > 0: TAG_62_val += "{}{:02}{}".format("04", len(TAG_6204["value"]), TAG_6204["value"])

			TAG_6205 = QRObj.get("AdditionalDataFieldTemplate||ReferenceLabel")
			if TAG_6205["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6205["value"]) > 0: TAG_62_val += "{}{:02}{}".format("05", len(TAG_6205["value"]), TAG_6205["value"])

			TAG_6206 = QRObj.get("AdditionalDataFieldTemplate||CustomerLabel")
			if TAG_6206["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6206["value"]) > 0: TAG_62_val += "{}{:02}{}".format("06", len(TAG_6206["value"]), TAG_6206["value"])

			TAG_6207 = QRObj.get("AdditionalDataFieldTemplate||TerminalLabel")
			if TAG_6207["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6207["value"]) > 0: TAG_62_val += "{}{:02}{}".format("07", len(TAG_6207["value"]), TAG_6207["value"])

			TAG_6208 = QRObj.get("AdditionalDataFieldTemplate||PurposeOfTransaction")
			if TAG_6208["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6208["value"]) > 0: TAG_62_val += "{}{:02}{}".format("08", len(TAG_6208["value"]), TAG_6208["value"])

			TAG_6209 = QRObj.get("AdditionalDataFieldTemplate||AdditionalConsumerDataRequest")
			if TAG_6209["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6209["value"]) > 0: TAG_62_val += "{}{:02}{}".format("09", len(TAG_6209["value"]), TAG_6209["value"])

			QR_String += "{}{:02}{}".format("62", len(TAG_62_val), TAG_62_val)

		TAG_64 = QRObj.get("MerchantInformation_LanguageTemplate")
		if TAG_64["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_64["value"]) > 0:
			TAG_64_val = ""
			TAG_6400 = QRObj.get("MerchantInformation_LanguageTemplate||LanguagePreference")
			if TAG_6400["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6400["value"]) > 0: TAG_64_val += "{}{:02}{}".format("00", len(TAG_6400["value"]), TAG_6400["value"])

			TAG_6401 = QRObj.get("MerchantInformation_LanguageTemplate||MerchantName_AlternateLanguage")
			if TAG_6401["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6401["value"]) > 0: TAG_64_val += "{}{:02}{}".format("01", len(TAG_6401["value"]), TAG_6401["value"])

			TAG_6402 = QRObj.get("MerchantInformation_LanguageTemplate||MerchantCity_AlternateLanguage")
			if TAG_6402["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_6402["value"]) > 0: TAG_64_val += "{}{:02}{}".format("02", len(TAG_6402["value"]), TAG_6402["value"])

			QR_String += "{}{:02}{}".format("62", len(TAG_64_val), TAG_64_val)

		if self.QR_Type == "MoMo":
			TAG_80 = QRObj.get("LastThreeDigitsOfPhoneNumber")
			if TAG_80["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_80["value"]) > 0: QR_String += "{}{:02}{}".format("80", len(TAG_80["value"]), TAG_80["value"])

		if self.QR_Type in ["KHQR_Individual", "KHQR_Corporate"]:
			TAG_99 = QRObj.get("Timestamp")
			if TAG_99["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_99["value"]) > 0:
				TAG_99_val = ""
				TAG_9900 = QRObj.get("Timestamp||timestamp")
				if TAG_9900["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_9900["value"]) > 0: TAG_99_val += "{}{:02}{}".format("00", len(TAG_9900["value"]), TAG_9900["value"])

				QR_String += "{}{:02}{}".format("99", len(TAG_99_val), TAG_99_val)

		for unknownKey in QRObj.filter_keys("^UnknownField").getObject():
			QR_String += QRObj.get(unknownKey)["value"]

		if update_CRC:
			QR_String += "6304"
			QR_String += calculate_crc16_ccitt_false(QR_String)
		else:
			TAG_63 = QRObj.get("CRC")
			if TAG_63["value"] != "JSON_DUPLICATE_KEYS_ERROR" and len(TAG_63["value"]) > 0: QR_String += "{}{:02}{}".format("63", len(TAG_63["value"]), TAG_63["value"])

		return QR_String