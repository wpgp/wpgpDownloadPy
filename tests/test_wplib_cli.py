#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wpgpDownload` package."""

import pytest
from click.testing import CliRunner

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


from wpgpDownload import cli

# NUMBER_OF_VALID_COUNTRIES = 249
THIS_FOLDER = Path(__file__).parent.as_posix()


@pytest.fixture
def number_of_valid_countries():
    return 249


class TestCli(object):

    def test_command_line_interface(self):
        """Test the CLI."""
        result = CliRunner().invoke(cli.wpgp_download)
        assert result.exit_code == 0
        assert 'wpgpDownload' in result.output
        help_result = CliRunner().invoke(cli.wpgp_download, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit' in help_result.output

    def test_cli_isos(self):
        import json

        isos_result_screen = CliRunner().invoke(cli.wpgp_download, ['isos'], input='yes')
        assert isos_result_screen.exit_code == 0
        assert '832,JEY,Jersey' in isos_result_screen.output
        isos_result_json = CliRunner().invoke(cli.wpgp_download, ['isos', '-f', 'json'])
        assert isos_result_json.exit_code == 0
        j = json.loads(isos_result_json.output)
        assert len(j) == number_of_valid_countries()
        grc = j.get('GRC', None)
        assert grc is not None
        assert len(grc) == 3
        assert grc[0] == '300'
        assert grc[1] == 'GRC'
        assert grc[2] == 'Greece'

    def test_cli_download(self):
        result = CliRunner().invoke(cli.wpgp_download, ['download', '--iso', 'VVV', '--datasets'])  # does not exist
        assert result.exit_code == 1
        result = CliRunner().invoke(cli.wpgp_download, ['download', '--iso', 'GRC', '--datasets'])
        assert result.exit_code == 0
        assert 'grc' in result.output
        result = CliRunner().invoke(cli.wpgp_download, ['download', '--iso', 'GRC', '--datasets', '--id', 91, '--id', '3577'])
        assert result.exit_code == 0
        assert '91' in result.output
        assert '3577' in result.output

    def test_cli_download_filter(self,):
        result = CliRunner().invoke(cli.wpgp_download, ['download', '--iso', 'GRC', '--datasets', '-f', 'grid-cell'])
        assert result.exit_code == 0
        assert 'Estimated total number of people per grid-cell 2000' in result.output
        assert 'Distance' not in result.output

    def test_cli_download_file(self,):
        result = CliRunner().invoke(cli.wpgp_download, ['download', '--iso', 'GRC', '--id', 20218, '--id', '20231'])
        assert result.exit_code == 0
