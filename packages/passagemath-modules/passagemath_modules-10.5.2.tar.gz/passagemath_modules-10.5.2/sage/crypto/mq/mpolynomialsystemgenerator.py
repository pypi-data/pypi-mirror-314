# sage_setup: distribution = sagemath-modules
"""
Abstract base class for generators of polynomial systems

AUTHOR:

Martin Albrecht <malb@informatik.uni-bremen.de>
"""
from sage.structure.sage_object import SageObject


class MPolynomialSystemGenerator(SageObject):
    """
    Abstract base class for generators of polynomial systems.
    """

    def __getattr__(self, attr):
        """
        EXAMPLES::

            sage: from sage.crypto.mq.mpolynomialsystemgenerator import MPolynomialSystemGenerator
            sage: msg = MPolynomialSystemGenerator()
            sage: msg.R
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        if attr == "R":
            self.R = self.ring()
            return self.R
        raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__,attr))

    def varformatstr(self, name):
        """
        Return format string for a given name 'name' which is
        understood by print et al.

        Such a format string is used to construct variable
        names. Typically those format strings are somewhat like
        'name%02d%02d' such that rounds and offset in a block can be
        encoded.

        INPUT:

        - ``name`` -- string

        EXAMPLES::

            sage: from sage.crypto.mq.mpolynomialsystemgenerator import MPolynomialSystemGenerator
            sage: msg = MPolynomialSystemGenerator()
            sage: msg.varformatstr('K')
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError

    def varstrs(self, name, round):
        """
        Return a list of variable names given a name 'name' and an
        index 'round'.

        This function is typically used by self._vars.

        INPUT:

        - ``name`` -- string
        - ``round`` -- integer index

        EXAMPLES::

            sage: from sage.crypto.mq.mpolynomialsystemgenerator import MPolynomialSystemGenerator
            sage: msg = MPolynomialSystemGenerator()
            sage: msg.varstrs('K', i)                                                   # needs sage.all
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError

    def vars(self, name, round):
        """
        Return a list of variables given a name 'name' and an
        index 'round'.

        INPUT:

        - ``name`` -- string
        - ``round`` -- integer index

        EXAMPLES::

            sage: from sage.crypto.mq.mpolynomialsystemgenerator import MPolynomialSystemGenerator
            sage: msg = MPolynomialSystemGenerator()
            sage: msg.vars('K',0)
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError

    def ring(self):
        """
        Return the ring in which the system is defined.

        EXAMPLES::

            sage: from sage.crypto.mq.mpolynomialsystemgenerator import MPolynomialSystemGenerator
            sage: msg = MPolynomialSystemGenerator()
            sage: msg.ring()
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError

    def block_order(self):
        """
        Return a block term ordering for the equation systems
        generated by ``self``.

        EXAMPLES::

            sage: from sage.crypto.mq.mpolynomialsystemgenerator import MPolynomialSystemGenerator
            sage: msg = MPolynomialSystemGenerator()
            sage: msg.block_order()
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError

    def __call__(self, P, K):
        """
        Encrypt plaintext P using the key K.

        INPUT:

        - ``P`` -- plaintext (vector, list)
        - ``K`` -- key (vector, list)

        EXAMPLES::

            sage: from sage.crypto.mq.mpolynomialsystemgenerator import MPolynomialSystemGenerator
            sage: msg = MPolynomialSystemGenerator()
            sage: msg(None, None)
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError

    def sbox(self):
        """
        Return SBox object for ``self``.

        EXAMPLES::

            sage: from sage.crypto.mq.mpolynomialsystemgenerator import MPolynomialSystemGenerator
            sage: msg = MPolynomialSystemGenerator()
            sage: msg.sbox()
            Traceback (most recent call last):
            ...
            AttributeError: '<class 'sage.crypto.mq.mpolynomialsystemgenerator.MPolynomialSystemGenerator'>' object has no attribute '_sbox'...
        """
        return self._sbox

    def polynomial_system(self, P=None, K=None):
        """
        Return a tuple F,s for plaintext P and key K where F is an
        polynomial system and s a dictionary which maps key variables
        to their solutions.

        INPUT:

        - ``P`` -- plaintext (vector, list)
        - ``K`` -- key (vector, list)

        EXAMPLES::

            sage: from sage.crypto.mq.mpolynomialsystemgenerator import MPolynomialSystemGenerator
            sage: msg = MPolynomialSystemGenerator()
            sage: msg.polynomial_system()
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError

    def random_element(self):
        """
        Return random element. Usually this is a list of elements in
        the base field of length 'blocksize'.

        EXAMPLES::

            sage: from sage.crypto.mq.mpolynomialsystemgenerator import MPolynomialSystemGenerator
            sage: msg = MPolynomialSystemGenerator()
            sage: msg.random_element()
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError
