import qtl_sopt_api as m


def test_basic():
    print(m)


def test_consts():
    print(m.consts)

    print(f'THOST_TERT_QUICK: {m.consts.THOST_TERT_QUICK}')
    print(f'THOST_FTDC_ICT_TaxNo: {m.consts.THOST_FTDC_ICT_TaxNo}')
    print(f'THOST_FTDC_FC_ExitEmergency: {m.consts.THOST_FTDC_FC_ExitEmergency}')


if __name__ == '__main__':
    test_basic()
    test_consts()
