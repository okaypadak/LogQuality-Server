

class Parse:
    @staticmethod
    def get_json_values(self, json_str, variable_name):
        try:
            data = json.loads(json_str)
            value = data.get(variable_name)

            if value is not None:
                return value
            else:
                logging.error(f"{variable_name} bulunamadı.")

        except json.JSONDecodeError as e:
            logging.error(f"Hata: JSON .. {e}")