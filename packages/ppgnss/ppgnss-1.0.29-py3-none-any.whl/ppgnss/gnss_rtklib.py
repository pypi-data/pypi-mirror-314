"""
   gnss_rtklib
   ------------------

   RTKLIB module of ppgnss. Use RTKLIB with python.
"""


def post_ppp(obs_file, brdc_file, sp3_file, clk_file, cfg_file):
    """Do PPP using ``rnx2rtkp``.

    :param obs_file: Observation file.
    :type obs_file: string
    :param
    """
    cmdline = '%s -k %s  %s %s %s %s -o %s' % (
        rtk_bin_prog, conf_filename, obs_filename,
        brdc_filename, sp3_filename, clk_filename, solution_fn)
