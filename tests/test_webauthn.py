import pytest

from auth.webauthn import (
    verify_registration,
    verify_assertion,
    uv_ok,
    sign_count_ok,
    credential_for_tenant
)


def test_registration():
    r = {'challenge': 'c1', 'origin': 'https://app.example', 'rp_id': 'app.example', 'credential_id': 'k1'}
    assert verify_registration(r, 'c1', 'https://app.example', 'app.example') is True

def test_registration_challenge():
    r = {'challenge': 'c2', 'origin': 'https://app.example', 'rp_id': 'app.example', 'credential_id': 'k1'}
    assert verify_registration(r, 'c1', 'https://app.example', 'app.example') is False

def test_registration_origin():
    r = {'challenge': 'c1', 'origin': 'https://evil.example', 'rp_id': 'app.example', 'credential_id': 'k1'}
    assert verify_registration(r, 'c1', 'https://app.example', 'app.example') is False

def test_registration_rp():
    r = {'challenge': 'c1', 'origin': 'https://app.example', 'rp_id': 'evil.example', 'credential_id': 'k1'}
    assert verify_registration(r, 'c1', 'https://app.example', 'app.example') is False

def test_assertion():
    r = {'challenge': 'c1', 'origin': 'https://app.example', 'rp_id': 'app.example', 'credential_id': 'k1', 'uv': True, 'sign_count': 5}
    stored = {'credential_id': 'k1', 'sign_count': 3}
    assert verify_assertion(r, 'c1', 'https://app.example', 'app.example', stored) is True

def test_uv_required():
    assert uv_ok(False, True) is False

def test_uv_ok():
    assert uv_ok(True, True) is True

def test_counter_up():
    assert sign_count_ok({'sign_count': 3}, 4) is True

def test_counter_down():
    assert sign_count_ok({'sign_count': 3}, 2) is False

def test_counter_zero():
    assert sign_count_ok({'sign_count': 0}, 0) is True

def test_tenant():
    store = {('t1', 'k1'): {'id': 'k1'}}
    assert credential_for_tenant(store, 't1', 'k1') == {'id': 'k1'}

def test_cross_tenant():
    store = {('t1', 'k1'): {'id': 'k1'}}
    assert credential_for_tenant(store, 't2', 'k1') is None

def test_unknown():
    assert credential_for_tenant({}, 't1', 'k1') is None

def test_empty_registration():
    assert verify_registration({}, 'c1', 'https://app.example', 'app.example') is False

def test_cloned():
    r = {'challenge': 'c1', 'origin': 'https://app.example', 'rp_id': 'app.example', 'credential_id': 'k1', 'uv': True, 'sign_count': 3, 'cloned': True}
    assert verify_assertion(r, 'c1', 'https://app.example', 'app.example', {'sign_count': 3}) is False
