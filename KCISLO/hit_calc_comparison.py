#type: ignore
import model

if __name__ == "__main__":
    pixel_size = 75
    electrons_num = 2200
    hit_pos = 45
    fig_size = 40

    px_model = model.PixelChargeSharingModel1D(pixel_size)
    print(f"{px_model.sigma=} μm")

    for hit_pos in range(0, 75, 10):
        px_model.hit(hit_pos, electrons_num)
        calc_hit_ideal = px_model.calc_hit_1D_ideal()

        print("")
        print(f"{hit_pos=} μm")
        print(f" {calc_hit_ideal=:.5f} μm")

        for order in [5]:
            calc_hit_Taylor = px_model.calc_hit_1D_taylor(order)
            print(f"{calc_hit_Taylor=:.5f} μm ({order=})")

        for lut_size in [10000]:
            calc_hit_lut = px_model.calc_hit_1D_lut(lut_size)
            print(f"   {calc_hit_lut=:.5f} μm ({lut_size=})")
