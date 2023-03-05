class Paper:
    one = {
        "pixel_size": 75,
        "charge_cloud_sigma": 6.31,
        "num_of_charges": 2200,
        "noise_sigma": 50,
    }
    two = {
        "pixel_size": 100,
        "charge_cloud_sigma": 16,
        "num_of_charges": 4970,
        "noise_sigma": 200,
    }
    three ={
        "pixel_size": 50,
        "charge_cloud_sigma": 6.31,
        "num_of_charges": 2200,
        "noise_sigma": 50,
    }
    four = {
        "pixel_size": 50,
        "charge_cloud_sigma": 16,
        "num_of_charges": 4970,
        "noise_sigma": 200,
    }

    @staticmethod
    def get_str(dict: dict[str, float]) -> str:
        return (
            f"""pixel size = {dict["pixel_size"]}μm, charge cloud σ = {dict["charge_cloud_sigma"]}μm\n"""
            f"""number of charges = {dict["num_of_charges"]}e, noise σ = {dict["noise_sigma"]}e RMS"""
        )

    @staticmethod
    def get_str_cloud_test(dict: dict[str, float]) -> str:
        return (
            f"""pixel size = {dict["pixel_size"]}μm, charge cloud σ in testing\n"""
            f"""number of charges = {dict["num_of_charges"]}e, noise σ = {dict["noise_sigma"]}e RMS"""
        )
