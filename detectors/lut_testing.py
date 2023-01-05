class LutTesting:
    one = {
        "pixel_size": 100,
        "charge_cloud_sigma": 15,
        "num_of_charges": 4970,
        "noise_sigma": 200,
    }
    two = {
        "pixel_size": 100,
        "charge_cloud_sigma": 25,
        "num_of_charges": 4970,
        "noise_sigma": 200,
    }
    three ={
        "pixel_size": 100,
        "charge_cloud_sigma": 35,
        "num_of_charges": 4970,
        "noise_sigma": 200,
    }
    four = {
        "pixel_size": 100,
        "charge_cloud_sigma": 45,
        "num_of_charges": 4970,
        "noise_sigma": 200,
    }
    five = {
        "pixel_size": 100,
        "charge_cloud_sigma": 55,
        "num_of_charges": 4970,
        "noise_sigma": 200,
    }

    @staticmethod
    def get_str(dict: dict[str, float]) -> str:
        return (
            f"""pixel size = {dict["pixel_size"]}μm, charge cloud σ = {dict["charge_cloud_sigma"]}μm\n"""
            f"""number of charges = {dict["num_of_charges"]}e, noise σ = {dict["noise_sigma"]}e RMS"""
        )
