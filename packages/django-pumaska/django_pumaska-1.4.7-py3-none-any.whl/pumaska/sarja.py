# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

from collections.abc import Iterable
import functools
import re

from django.db.models import ProtectedError
from django import forms
from django.template import loader
from django.utils.translation import gettext_lazy as _
from django import VERSION as django_versio

from .nidottu import yhdistetty_lomake


# Mallin nimen poiminta Djangon ProtectedError-poikkeusoliosta.
# Ks. django/db/models/deletion.py; `Collector.collect`-metodi.
mallin_nimi = re.compile(r'Cannot delete some instances of model ([^ ]+)')


@functools.wraps(yhdistetty_lomake)
def lisaa_lomakesarja(
  LomakeA, LomakeB,
  *,
  avain_a=None,
  avain_b=None,
  tunnus=None,
  epasuora=False,
  pakollinen=False,
  lomakesarja_parametrit=None,
  valita_parametrit: Iterable = (),
  **kwargs
):
  '''
  Yhdistää ModelForm-luokan ja toisesta ModelForm-luokasta
  muodostetun InlineFormSet-luokan silloin,
  kun B-luokasta on suora (ForeignKey) tai epäsuora (GenericForeignKey)
  viittaus A-luokkaan.

  Args:
    LomakeA, LomakeB: mallikohtaiset lomakeluokat
    avain_a, avain_b: viittaukset mallien välillä
    tunnus: yksikäsitteinen tunnus lomakesarjalle (oletus 'lomakesarja')
    epasuora: käytetään `generic_inlineformset_factory`-funktiota?
    lomakesarja_parametrit: parametrit, jotka asetetaan lomakesarjan määreiksi
    valita_parametrit: ulomman lomakkeen parametrit, jotka välitetään
      sellaisenaan lomakesarjalle
    *args, **kwargs: lisäparametrit ``inlineformset_factory``-funktiolle

  Returns:
    lomakeluokka
  '''
  # Pakotetaan ylimääräisten lomakkeiden määräksi nolla.
  kwargs['extra'] = 0

  assert tunnus or avain_a or avain_b, (
    'Joko `tunnus`, `avain_a` tai `avain_b` on määriteltävä.'
  )

  if epasuora:
    from django.contrib.contenttypes.forms import generic_inlineformset_factory
    lomakesarja = generic_inlineformset_factory(
      LomakeB.Meta.model,
      form=LomakeB,
      **kwargs
    )
  else:
    lomakesarja = forms.models.inlineformset_factory(
      LomakeA.Meta.model,
      LomakeB.Meta.model,
      form=LomakeB,
      **kwargs
    )

  # Käytetään tyhjän lomakkeen oletusarvoina
  # `initial`-datan ensimmäistä alkiota.
  class lomakesarja(lomakesarja):
    # pylint: disable=function-redefined
    def get_form_kwargs(self, index):
      if index is None and self.initial_extra:
        return {
          **super().get_form_kwargs(index), 'initial': self.initial_extra[0]
        }
      else:
        return super().get_form_kwargs(index)
      # def get_form_kwargs
    # class lomakesarja

  # Aseta mahdolliset lomakesarjan parametrit.
  for avain, arvo in (lomakesarja_parametrit or {}).items():
    setattr(lomakesarja, avain, arvo)

  # Lisää tarvittaessa oletusarvot HTML-piirtoa varten.
  if not hasattr(lomakesarja, 'label'):
    lomakesarja.label = (
      LomakeB.Meta.model._meta.verbose_name_plural
    ).capitalize()
  if not hasattr(lomakesarja, 'palikka'):
    lomakesarja.palikka = 'pumaska/lomakesarja_lomakekenttana.html'
  if not hasattr(lomakesarja, 'riviluokka'):
    lomakesarja.riviluokka = 'panel panel-default clearfix'
  if not hasattr(lomakesarja, 'lisaa_painike'):
    lomakesarja.lisaa_painike = _('Lisää %(malli)s') % {
      'malli': LomakeB.Meta.model._meta.verbose_name
    }
  if not hasattr(lomakesarja, 'poista_painike'):
    lomakesarja.poista_painike = _('Poista %(malli)s') % {
      'malli': LomakeB.Meta.model._meta.verbose_name
    }

  tunnus = tunnus or avain_a or (
    LomakeB.Meta.model._meta.get_field(avain_b).remote_field.name
  )

  if tunnus in LomakeA.base_fields:
    raise RuntimeError(
      f'Lomakesarjaa ei voida nitoa samalla nimellä'
      f' kuin olemassaoleva lomakekenttä: {tunnus}'
    )

  def liitos_kwargs(self: LomakeA):
    '''
    Korvataan oletusarvoinen, ulommasta initial-datasta poimittu
    `initial` luetteloksi käärityllä versiolla.

    Asetetaan ulompi olio lomakesarjan `instanceksi`.
    '''
    initial = {
      avain.replace(tunnus + '-', '', 1): arvo
      for avain, arvo in self.initial.items()
      if avain.startswith(tunnus + '-') and avain != tunnus + '-'
    }
    assert isinstance(self.instance, self.Meta.model), (
      f'Kohde A ei voi olla tyyppiä {type(self.instance)} != {self.Meta.model}!'
    )
    return {
      'initial': [initial] if initial else [],
      'instance': self.instance,
      'queryset': (
        getattr(self.instance, avain_a).all()
        if avain_a and self.instance.pk
        else None
      ),
    }
    # def liitos_kwargs

  YhdistettyLomake = lisaa_lomakesarja.__wrapped__(
    LomakeA, lomakesarja,
    tunnus=tunnus,
    liitos_kwargs=liitos_kwargs,
    valita_parametrit=valita_parametrit,
    pakollinen=pakollinen,
  )
  @functools.wraps(YhdistettyLomake, updated=())
  class YhdistettyLomake(YhdistettyLomake):
    # pylint: disable=function-redefined

    # HTML (Django 4-)

    if django_versio < (5, ):
      def _html_output(self, *args, **kwargs):
        '''
        Tuotetaan super-tuloste (A-lomake) sekä lomakesarjan perustoteutus:
        - kukin olemassaoleva B-lomake,
        - tyhjä B-lomake uuden lisäämiseksi,
        - hallintolomake ja
        - tarvittava Javascript rivien poistoon ja lisäämiseen.
        '''
        # pylint: disable=protected-access
        return super()._html_output(*args, **kwargs) \
        + loader.get_template('pumaska/lomakesarja.html').render({
          'tunnus': tunnus,
          'lomakesarja': getattr(self, tunnus),
        })
        # def _html_output


    # ModelForm

    def _save_m2m(self):
      '''
      Tallennetaan M2M-kohteet `super`-toteutuksen mukaisesti.
      Tämän jälkeen tallennetaan lomakesarja.

      Mikäli olemassaolevien rivien poisto epäonnistuu mallin tasolla
      `ProtectedError`-poikkeuksen takia, parsitaan tämän poikkeuksen
      viestitekstistä riippuvan mallin nimi ja tuotetaan vastaava
      `ValidationError`.
      '''
      super()._save_m2m()
      lomakesarja = getattr(self, tunnus)
      lomakesarja.instance = self.instance
      try:
        with self.tallenna_liitos(tunnus):
          lomakesarja.save(commit=True)
      except ProtectedError as exc:
        try:
          _mallin_nimi = mallin_nimi.match(str(exc))[1]
        except (TypeError, KeyError):
          exc2 = forms.ValidationError(str(exc), code='protect')
        else:
          exc2 = forms.ValidationError(
            _(
              'Rivin poisto epäonnistui:'
              ' suojattuja, riippuvia %(malli)s-kohteita.'
            ) % {'malli': _mallin_nimi},
            code='protect',
          )
        lomakesarja._non_form_errors.append(exc2)
        raise exc2 from exc
      # def _save_m2m

    # class YhdistettyLomake

  return YhdistettyLomake
  # def lisaa_lomakesarja
